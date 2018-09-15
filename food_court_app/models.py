from django.db import models
from django.utils import timezone

import hashlib

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
    mail = models.EmailField(default='*@*')
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
    orderDetail_id = models.AutoField(primary_key=True)
    menu_id = models.ForeignKey(
            'MENU', 
            to_field='menu_id', 
            related_name='fromOrderDetail_menuId',  
            on_delete=models.CASCADE
            )  
    order_qty = models.IntegerField(default=1)
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

def get_image_path(instance, filename):
    return "store_image/%s" % (instance.store_name + ".png")
        
class STORE(models.Model):    
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(
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
            
class MENU(models.Model):  
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(
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

    def __str__(self):
        return str(self.menu_id)
            
class MENU_TYPE(models.Model):  
    menu_type_id = models.AutoField(primary_key=True)
    menu_type_name = models.CharField(
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