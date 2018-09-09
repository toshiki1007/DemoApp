from django.db import models
from django.utils import timezone

class AREA(models.Model):
    areaId = models.IntegerField(
            primary_key=True
            )
    xCoordinate = models.IntegerField(
            blank=False, 
            null=False,
            default = 0
            )
    yCoordinate = models.IntegerField(
            blank=False, 
            null=False,
            default = 0
            )

class TABLE(models.Model):
    tableId = models.IntegerField(primary_key=True)
    seatsNum = models.IntegerField(default=4)
    areaId = models.ForeignKey(
            'AREA', 
            to_field='areaId', 
            related_name='fromTable_areaId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            )
            
class TABLE_STATUS(models.Model):
    reservationId = models.IntegerField(primary_key=True)
    reservationDateTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    startDateTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    endDateTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    cancelFlg = models.BooleanField(default=False)        
    tableId = models.ForeignKey(
            'TABLE', 
            to_field='tableId', 
            related_name='fromTabaleStatus_tableId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            )        
    
class ORDER(models.Model):
    orderId = models.IntegerField(
            blank=False, 
            null=False,
            primary_key=True
            )
    orderDateTime = models.DateTimeField(
            blank=False, 
            null=False
            )
    totalPrice = models.IntegerField(
            blank=False, 
            null=False,
            default=0
            )
    orderStatus = models.CharField(max_length=2)
    mailAddress = models.EmailField(default='*@*')
    reservationId = models.ForeignKey(
            'TABLE_STATUS', 
            to_field='reservationId', 
            related_name='fromOrder_reservationId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            ) 

class ORDER_DETAIL(models.Model):
    orderDetailId = models.IntegerField(primary_key=True)
    menuId = models.ForeignKey(
            'MENU', 
            to_field='menuId', 
            related_name='fromOrderDetail_menuId',  
            on_delete=models.CASCADE
            )  
    orderNum = models.IntegerField(default=1)
    orderStatus = models.CharField(max_length=2)
    provideDateTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    cancelFlg = models.BooleanField(default=False) 
    orderId = models.ForeignKey(
            'ORDER', 
            to_field='orderId', 
            related_name='fromOrderDetail_orderId',
            on_delete=models.CASCADE
            )    
    
class SHOP(models.Model):    
    shopId = models.IntegerField(primary_key=True)
    shopName = models.CharField(
            max_length=50, 
            blank=False, 
            null=False
            )
    openDateTime = models.DateTimeField(
            blank=False, 
            null=False
            )
    closeDateTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    areaId = models.ForeignKey(
            'AREA', 
            to_field='areaId', 
            related_name='fromShop_areaId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            ) 
    
class MENU(models.Model):  
    menuId = models.IntegerField(primary_key=True)
    menuName = models.CharField(
            max_length=20,
            blank=False, 
            null=False
            )
    menuType = models.CharField(
            max_length=5,
            blank=False, 
            null=False,
            default='00000'
            )
    price = models.IntegerField(
            blank=False, 
            null=False,
            default = 0
            )
    estTime = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    shopId = models.ForeignKey(
            'SHOP', 
            to_field='shopId', 
            related_name='fromMenu_shopId',              
            on_delete=models.CASCADE
            )