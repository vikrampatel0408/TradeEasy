# Generated by Django 4.0 on 2023-04-14 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0012_stock_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='tokens_invested',
        ),
        migrations.AlterField(
            model_name='stock',
            name='Quantity',
            field=models.IntegerField(),
        ),
    ]