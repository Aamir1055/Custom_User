# Generated by Django 3.2.9 on 2022-10-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0004_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, verbose_name='email address'),
        ),
    ]
