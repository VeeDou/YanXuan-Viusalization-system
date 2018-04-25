from django.db import models
# from django.contrib.postgres.fields import JSONField
# from jsonfield import JSONField
from django_mysql.models import JSONField, Model


# Create your models here.
# def get_default_data():
#     return { 'name':'Model' }

 

class Goods(models.Model):
    itemid = models.IntegerField()
    updated = models.DateTimeField()
    detail = JSONField()
    comments = models.TextField()
    itemid_typeA = models.IntegerField()
    itemid_typeB = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    comments_num = models.IntegerField()
    say_good_pct = models.DecimalField(max_digits=3, decimal_places=2)
    seem_good_tag =models.IntegerField()
    seem_cheap_tag =models.IntegerField()
    comments_tags  = JSONField()
 
    class Meta:
        managed = False
        db_table = 'goods_yanxuan'