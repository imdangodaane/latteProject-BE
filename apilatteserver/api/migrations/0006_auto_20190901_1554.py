# Generated by Django 2.2.4 on 2019-09-01 08:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190831_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_carousel',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='token',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 1, 8, 54, 16, 666990, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='expired_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 1, 9, 9, 16, 667014, tzinfo=utc), null=True),
        ),
    ]