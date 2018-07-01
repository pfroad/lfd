# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=16)
    mobile = models.CharField(max_length=16)
    sex = models.IntegerField(blank=True, null=True, default=0)
    birthday = models.DateField(blank=True, null=True)
    mail = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    nick_name = models.CharField(max_length=32, blank=True, null=True)
    avatar = models.CharField(max_length=32, blank=True, null=True)
    is_deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_disabled = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
