# Generated by Django 4.0.3 on 2022-04-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0005_crypto_tbl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto_tbl',
            name='b_amt',
            field=models.FloatField(),
        ),
    ]
