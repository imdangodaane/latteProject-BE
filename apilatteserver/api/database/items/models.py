from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class ItemDb(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name_english = models.CharField(unique=True, max_length=50)
    name_japanese = models.CharField(max_length=50)
    type = models.PositiveIntegerField()
    price_buy = models.PositiveIntegerField(blank=True, null=True)
    price_sell = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField()
    attack = models.PositiveSmallIntegerField(blank=True, null=True)
    defence = models.PositiveSmallIntegerField(blank=True, null=True)
    range = models.PositiveIntegerField(blank=True, null=True)
    slots = models.PositiveIntegerField(blank=True, null=True)
    equip_jobs = models.BigIntegerField(blank=True, null=True)
    equip_upper = models.PositiveIntegerField(blank=True, null=True)
    equip_genders = models.PositiveIntegerField(blank=True, null=True)
    equip_locations = models.PositiveIntegerField(blank=True, null=True)
    weapon_level = models.PositiveIntegerField(blank=True, null=True)
    equip_level = models.PositiveIntegerField(blank=True, null=True)
    refineable = models.PositiveIntegerField(blank=True, null=True)
    view = models.PositiveSmallIntegerField(blank=True, null=True)
    script = models.TextField(blank=True, null=True)
    equip_script = models.TextField(blank=True, null=True)
    unequip_script = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_db'