from django.db import models
from django.utils import timezone

class TABLE(models.Model):
    tableId = models.AutoField(primary_key=True)
    seaqty = models.IntegerField(default=4)
    
    def __str__(self):
        return str(self.tableId)
            
class RESERVE_TABLE(models.Model):
    reservationId = models.AutoField(primary_key=True)
    reservationTime = models.DateTimeField(
            auto_now_add=True,
            blank=True, 
            null=True
            )
    startTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    endTime = models.DateTimeField(
            blank=True, 
            null=True
            )
    cancelFlg = models.BooleanField(default=False)        
    tableId = models.ForeignKey(
            'TABLE', 
            to_field='tableId', 
            related_name='fromReserveTable_tableId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            )
    
    def __str__(self):
        return str(self.reservationId)

class ORDER(models.Model):
    orderId = models.AutoField(primary_key=True)
    orderTime = models.DateTimeField(
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
    reservationId = models.ForeignKey(
            'RESERVE_TABLE', 
            to_field='reservationId', 
            related_name='fromOrder_reservationId',
            blank=False, 
            null=False,
            on_delete=models.CASCADE
            ) 
            
    def __str__(self):
        return str(self.orderId)

class ORDER_DETAIL(models.Model):
    orderDetailId = models.AutoField(primary_key=True)
    menuId = models.ForeignKey(
            'MENU', 
            to_field='menuId', 
            related_name='fromOrderDetail_menuId',  
            on_delete=models.CASCADE
            )  
    orderQty = models.IntegerField(default=1)
    supplyTime = models.DateTimeField(
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
        
class STORE(models.Model):    
    storeId = models.AutoField(primary_key=True)
    storeName = models.CharField(
            max_length=50, 
            blank=False, 
            null=False
            )
    startDate = models.DateField(
            blank=True, 
            null=True
            )
    endDate = models.DateField(
            blank=True, 
            null=True
            )
            
    def __str__(self):
        return str(self.storeId)
            
class MENU(models.Model):  
    menuId = models.AutoField(primary_key=True)
    menuName = models.CharField(
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
    menuTypeId = models.ForeignKey(
            'MENU_TYPE', 
            to_field='menuTypeId', 
            related_name='fromMenu_menuTypeId',              
            on_delete=models.CASCADE,
            blank=False, 
            null=False
            )            
    #time型がないのでintにする（分数ならintで表現可）
    creationTime = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    orderableFlg = models.BooleanField(default=True) 
    storeId = models.ForeignKey(
            'STORE', 
            to_field='storeId', 
            related_name='fromMenu_storeId',              
            on_delete=models.CASCADE
            )

    def __str__(self):
        return str(self.menuId)
            
class MENU_TYPE(models.Model):  
    menuTypeId = models.AutoField(primary_key=True)
    menuTypeName = models.CharField(
            max_length=50,
            blank=False, 
            null=False
            )

    def __str__(self):
        return str(self.menuTypeId)
            
class MENU_CROWD(models.Model):  
    menuId = models.ForeignKey(
            'MENU', 
            to_field='menuId', 
            related_name='fromMenuCrowd_menuId',              
            on_delete=models.CASCADE,
            primary_key=True
            )
    watingTime = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    modifiedTime = models.DateTimeField(
            auto_now=True,
            blank=False, 
            null=False
            )
            
class STORE_CROWD(models.Model):  
    storeId = models.ForeignKey(
            'STORE', 
            to_field='storeId', 
            related_name='fromStoreCrowd_menuId',              
            on_delete=models.CASCADE,
            primary_key=True
            )
    watingTime = models.IntegerField(
            blank=False, 
            null=False,
            default = 1
            )
    crowdStatus = models.IntegerField(default=0)
    modifiedTime = models.DateTimeField(
            auto_now=True,
            blank=False, 
            null=False
            )