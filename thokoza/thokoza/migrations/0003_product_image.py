# Generated by Django 3.2.5 on 2021-07-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thokoza', '0002_rename_products_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
