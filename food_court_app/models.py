from django.db import models
from django.utils import timezone

from .consts import *

import hashlib
import uuid
import os

class TABLE(models.Model):
    table_id = models.AutoField(primary_key=True)
    seat_qty = models.IntegerField(default=4)
    
    def __str__(self):
        return str(self.table_id)
            
class RESERVE_TABLE(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    reservation_time = models.DateTimeField(
            auto_now_add=True,
            blank=True, 
            null=True
            )
    start_time = models.DateTimeField(
            blank=True, 
            null=True
            )
    end_time = models.DateTimeField(
            blank=True, 
            null=True
            )
    cancel_flg = models.BooleanField(default=False)        
    table_id = models.ForeignKey(
            'TABLE', 
            to_field='table_id', 
            related_name='fromReserveTable_tableId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            )
    
    def __str__(self):
        return str(self.reservation_id)

class ORDER(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_time = models.DateTimeField(
            auto_now_add=True,
            blank=True, 
            null=True
            )
    amount = models.DecimalField(
            blank=False, 
            null=False,
            max_digits=10,
            decimal_places=2,
            default=0
            )
    status = models.IntegerField(default=0)
    mail = models.EmailField(default='*@*',
            blank=False,
            null=False
            )
    reservation_id = models.ForeignKey(
            'RESERVE_TABLE', 
            to_field='reservation_id', 
            related_name='fromOrder_reservationId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            ) 
            
    def __str__(self):
        return str(self.order_id)

class ORDER_DETAIL(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    menu_id = models.ForeignKey(
            'MENU', 
            to_field='menu_id', 
            related_name='fromOrderDetail_menuId',  
            on_delete=models.CASCADE
            )  
    order_qty = models.IntegerField(default=0)
    supply_time = models.DateTimeField(
            blank=True, 
            null=True
            )
    cancel_flg = models.BooleanField(default=False) 
    order_id = models.ForeignKey(
            'ORDER', 
            to_field='order_id', 
            related_name='fromOrderDetail_orderId',
            on_delete=models.CASCADE
            )    

#保存ファイル名設定用メソッド
def get_image_path(instance, filename):
    file_name = str(uuid.uuid4())
    return "store_image/%s" % (file_name + PNG)

#古いファイルを削除する為のデコレータ
def delete_previous_file(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        
        if self.image_file == None:
            print("NONE")
        # 保存前のファイル名を取得
        result = STORE.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        
        super(STORE, self).save()
        result = function(*args, **kwargs)

        # 古いファイルが存在＆ファイル変更有りの場合のみ、古いファイルを削除
        if previous:
            if previous.image_file != self.image_file:
                 os.remove(MEDIA_ROOT + '/' + previous.image_file.name)
        return result
    return wrapper
        
class STORE(models.Model):   
    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, \
        update_fields=None):
        super(STORE, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(STORE, self).delete()
    
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(
            max_length=50, 
            blank=False, 
            null=False
            )
    store_name_english = models.CharField(
            max_length=50, 
            blank=False, 
            null=False
            )
    start_date = models.DateField(
            blank=True, 
            null=True
            )
    end_date = models.DateField(
            blank=True, 
            null=True
            )
    image_file = models.ImageField(upload_to=get_image_path,\
            blank=False, 
            null=False
            )
            
    def __str__(self):
        return str(self.store_id)

#古いファイルを削除する為のデコレータ
def delete_previous_file_menu(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        
        if self.image_file == None:
            print("NONE")
        # 保存前のファイル名を取得
        result = MENU.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        
        super(MENU, self).save()
        result = function(*args, **kwargs)

        # 古いファイルが存在＆ファイル変更有りの場合のみ、古いファイルを削除
        if previous:
            if previous.image_file != self.image_file:
                 os.remove(MEDIA_ROOT + '/' + previous.image_file.name)
        return result
    return wrapper
            
class MENU(models.Model):  
    @delete_previous_file_menu
    def save(self, force_insert=False, force_update=False, using=None, \
        update_fields=None):
        super(MENU, self).save()

    @delete_previous_file_menu
    def delete(self, using=None, keep_parents=False):
        super(MENU, self).delete()
    
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(
            max_length=50,
            blank=False, 
            null=False
            )
    menu_name_english = models.CharField(
            max_length=50,
            blank=False, 
            null=False
            )
    price = models.DecimalField(
            blank=False, 
            null=False,
            max_digits=10,
            decimal_places=2,
            default = 0
            )
    menu_type_id = models.ForeignKey(
            'MENU_TYPE', 
            to_field='menu_type_id', 
            related_name='fromMenu_menuTypeId',              
            on_delete=models.CASCADE,
            blank=False, 
            null=False
            )            
    #time型がないのでintにする（分数ならintで表現可）
    creation_time = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    orderable_flg = models.BooleanField(default=True) 
    store_id = models.ForeignKey(
            'STORE', 
            to_field='store_id', 
            related_name='fromMenu_storeId',              
            on_delete=models.CASCADE
            )
    image_file = models.ImageField(upload_to=get_image_path,\
            blank=False, 
            null=False
            )
    def __str__(self):
        return str(self.menu_id)
            
class MENU_TYPE(models.Model):  
    menu_type_id = models.AutoField(primary_key=True)
    menu_type_name = models.CharField(
            max_length=50,
            blank=False, 
            null=False
            )
    menu_type_name_english = models.CharField(
            max_length=50,
            blank=False, 
            null=False
            )

    def __str__(self):
        return str(self.menu_type_id)
            
class MENU_CROWD(models.Model):  
    menu_id = models.ForeignKey(
            'MENU', 
            to_field='menu_id', 
            related_name='fromMenuCrowd_menuId',              
            on_delete=models.CASCADE,
            primary_key=True
            )
    wating_time = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    modified_time = models.DateTimeField(
            auto_now=True,
            blank=False, 
            null=False
            )
            
class STORE_CROWD(models.Model):  
    store_id = models.ForeignKey(
            'STORE', 
            to_field='store_id', 
            related_name='fromStoreCrowd_menuId',              
            on_delete=models.CASCADE,
            primary_key=True
            )
    wating_time = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    crowd_status = models.IntegerField(default=0)
    modified_time = models.DateTimeField(
            auto_now=True,
            blank=False, 
            null=False
            )