# Generated by Django 3.0.8 on 2020-07-19 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_auto_20200715_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, default='', max_length=300),
        ),
    ]
