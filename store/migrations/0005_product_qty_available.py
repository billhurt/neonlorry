# Generated by Django 4.2.5 on 2023-11-25 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_product_qty_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qty_available',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
