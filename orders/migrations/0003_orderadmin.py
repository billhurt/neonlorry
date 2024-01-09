# Generated by Django 4.2.4 on 2024-01-02 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_billing_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAdmin',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.order')),
            ],
            bases=('orders.order',),
        ),
    ]
