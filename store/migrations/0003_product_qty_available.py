# Generated by Django 4.2.5 on 2023-11-20 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qty_available',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
