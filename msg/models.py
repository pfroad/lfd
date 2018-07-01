# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class SmsCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    mobile = models.CharField(max_length=16)
    code = models.CharField(max_length=256)
    verified = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    expired_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_code'