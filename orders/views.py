from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string

from basket.basket import Basket

from .models import Order, OrderItem, Product


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        ship_dict = dict(request.POST.items())
        full_name = ship_dict.get('data[0][value]')
        add1 = ship_dict.get('data[1][value]')
        add2 = ship_dict.get('data[2][value]', '')
        town_city = ship_dict.get('data[3][value]', '')
        county = ship_dict.get('data[4][value]', '')
        post_code = ship_dict.get('data[5][value]')
        billing_name = ship_dict.get('data[6][value]')
        email = ship_dict.get('data[7][value]')
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name=full_name, email=email, address1=add1,
                                address2=add2, city=town_city, county=county, post_code=post_code, total_paid=baskettotal, order_key=order_key, billing_name=billing_name)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Item successfully added to basket.'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
    order = Order.objects.filter(order_key=data)
    order_items = OrderItem.objects.all()
    for x in order:
        name = x.billing_name
        email = x.email
        order_id = x.pk
        total_paid = x.total_paid
        order_items = OrderItem.objects.filter(order_id=order_id)

        for item in order_items:
            product_id = item.product.id
            qty = item.quantity
            Product.objects.filter(id=product_id).update(qty_available=item.product.qty_available - qty)
            
    
    send_mail(
            'CC Tights - Order Confirmation' + ' Order ID: ' + str(order_id), 
            render_to_string('payment/order_confirmation_email.html', {
            'name': name,
            'order_items': order_items,
            'total_paid': total_paid,
            'order_id': order_id,
        }),
            'noreply@cctights.com',
            [email, 'orders@cctights.com'],
            fail_silently=False,
         ),


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})