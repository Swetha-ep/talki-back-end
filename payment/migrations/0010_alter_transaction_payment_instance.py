# Generated by Django 4.2.5 on 2023-11-01 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_alter_transaction_payment_instance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_instance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment.payment'),
        ),
    ]
