# Generated by Django 4.2.5 on 2023-10-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0012_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorapplication',
            name='country',
            field=models.CharField(default='India'),
        ),
    ]
