from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class Login(models.Model):
    account_id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255)
    user_pass = models.CharField(max_length=255)
    sex = models.CharField(max_length=1)
    email = models.CharField(max_length=255)
    group_id = models.IntegerField(default=0)
    state = models.PositiveIntegerField(default=0)
    unban_time = models.PositiveIntegerField(default=0)
    expiration_time = models.PositiveIntegerField(default=0)
    logincount = models.PositiveIntegerField(default=0)
    lastlogin = models.DateTimeField(blank=True, null=True)
    last_ip = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    character_slots = models.PositiveIntegerField(default=15)
    pincode = models.CharField(blank=True, max_length=4)
    pincode_change = models.PositiveIntegerField(default=0)
    vip_time = models.PositiveIntegerField(default=0)
    old_group = models.IntegerField(default=0)

    def __str__(self):
        return str(self.account_id) + self.userid

    class Meta:
        managed = False
        db_table = 'login'


# class User(models.Model):
#     account = models.ForeignKey(Login, on_delete=models.CASCADE)
#     token = models.CharField(max_length=255, blank=True, null=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#     expired_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=15))

#     def __str__(self):
#         return 'of userid: ' + str(self.user.account_id)


class Token(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now())
    expired_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=15), blank=True, null=True)

    def __str__(self):
        return 'of userid: ' + str(self.user.account_id)