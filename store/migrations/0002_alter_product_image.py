# Generated by Django 4.2.5 on 2023-11-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='images/airplane-fill.svg', upload_to='images/'),
        ),
    ]
