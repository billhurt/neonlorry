const stripe = Stripe('pk_test_51O9YfHKYG9KhsX3JI9qMys0hQ0lDd5nvcmxh7XdDWfAMX2Jwfb2pEEpqK4gUAHn4feDpdZECqJeVjQeeZrebFRxt00GovvkS0V')


const elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');


const elements = stripe.elements();
let style = {
    base: {
      color: "#000",
      lineHeight: '2.4',
      fontSize: '16px'
    }
    };


const card = elements.create('card', {'style': style });
card.mount('#card-element');

card.on('change', function(event) {
    const displayError = document.getElementById('error-message')
    if (event.error) {
      displayError.textContent = event.error.message;
      $('#error-message').addClass('alert alert-info');
    } else {
      displayError.textContent = '';
      $('#error-message').removeClass('alert alert-info');
    }
    });

let form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

let custName = document.getElementById("custName").value;
let email = document.getElementById("email").value;
let custAdd = document.getElementById("custAdd").value;
let custAdd2 = document.getElementById("custAdd2").value;
let townCity = document.getElementById("townCity").value;
let county = document.getElementById("county").value;
let dataString = $("#shipping-form, #payment-form").serializeArray()

  $.ajax({
      type: "POST",
      url: 'http://127.0.0.1:8000/orders/add/',
      data: {
        order_key: clientsecret,
        csrfmiddlewaretoken: CSRF_TOKEN,
        action: "post",
        data: dataString,
      },
      success: function (json) {
        console.log(json.success)
        console.log(dataString)

        stripe.confirmCardPayment(clientsecret, {
          payment_method: {
            card: card,
            billing_details: {
              address:{
                  line1:custAdd,
                  line2:custAdd2,
                  city:townCity,
                  state:county,
              },
              email: email,
              name: custName,
            },
          }
        }).then(function(result) {
          if (result.error) {
            console.log('payment error')
            console.log(result.error.message);
          } else {
            if (result.paymentIntent.status === 'succeeded') {
              console.log('payment processed')
              // There's a risk of the customer closing the window before callback
              // execution. Set up a webhook or plugin to listen for the
              // payment_intent.succeeded event that handles any business critical
              // post-payment actions.
              window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
            }
          }
        });

      },
      error: function (xhr, errmsg, err) {},
    });



});