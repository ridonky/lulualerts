# Generated by Django 4.0.4 on 2022-06-17 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lulu_alerts', '0002_alert_history_alerts_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alerts',
            name='status',
        ),
        migrations.AddField(
            model_name='alerts',
            name='status',
            field=models.ManyToManyField(related_name='alerts', to='lulu_alerts.alert_status'),
        ),
    ]
