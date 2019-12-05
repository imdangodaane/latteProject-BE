# Generated by Django 2.2.4 on 2019-08-31 16:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190831_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 31, 16, 50, 9, 670882, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='expired_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 31, 17, 5, 9, 670906, tzinfo=utc), null=True),
        ),
    ]