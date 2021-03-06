# Generated by Django 3.0.8 on 2020-07-15 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20200715_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='month',
            field=models.CharField(choices=[('On Queue', 'On Queue'), ('Printing', 'Printing'), ('Done', 'Done'), ('Received', 'Received')], default='On Queue', max_length=9),
        ),
        migrations.AlterField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='shops.Profile'),
        ),
    ]
