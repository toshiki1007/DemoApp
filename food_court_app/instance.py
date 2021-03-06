from .models import *

class table_status:
    def set(self , TABLE , status_flg):
        self.__table_id = TABLE.table_id
        self.__seat_qty = TABLE.seat_qty
        self.__status = status_flg     
        
        return self
    
    @property
    def table_id(self):
        return self.__table_id
        
    @property
    def seat_qty(self):
        return self.__seat_qty
        
    @property
    def status(self):
        return self.__status
        
        
class crowd_status:
    def set(self , STORE , STORE_CROWD , store_image_path):
        self.__store_id = STORE.store_id
        self.__store_name = STORE.store_name
        self.__start_date = STORE.start_date
        self.__end_date = STORE.end_date   
        self.__wating_time = STORE_CROWD.wating_time    
        self.__crowd_status = STORE_CROWD.crowd_status    
        self.__modified_time = STORE_CROWD.modified_time
        self.__store_image_path = store_image_path
        
        return self
   
    @property
    def store_id(self):
        return self.__store_id
        
    @property
    def store_name(self):
        return self.__store_name
        
    @property
    def start_date(self):
        return self.__start_date
        
    @property
    def end_date(self):
        return self.__end_date
        
    @property
    def wating_time(self):
        return self.__wating_time
        
    @property
    def crowd_status(self):
        return self.__crowd_status
    
    @property
    def modified_time(self):
        return self.__modified_time
        
    @property
    def store_image_path(self):
        return self.__store_image_path
        
class menu_and_store:
    def set(self , STORE , MENU , MENU_TYPE, STORE_CROWD):
        self.__menu_id = MENU.menu_id    
        self.__menu_name = MENU.menu_name
        self.__menu_name_english = MENU.menu_name_english
        self.__price = MENU.price
        self.__menu_type_name = MENU_TYPE.menu_type_name
        self.__menu_type_name_english = MENU_TYPE.menu_type_name_english   
        self.__creation_time = MENU.creation_time
        self.__store_name = STORE.store_name
        self.__store_name_english = STORE.store_name_english
        self.__store_id = STORE.store_id
        self.__image_file = MENU.image_file
        if (MENU.creation_time + STORE_CROWD.wating_time) < 15:
            self.__instantly = True
        else:
            self.__instantly = False
        return self    
        
    @property
    def menu_id(self):
        return self.__menu_id
        
    @property
    def menu_name(self):
        return self.__menu_name
        
    @property
    def menu_name_english(self):
        return self.__menu_name_english
        
    @property
    def price(self):
        return self.__price
        
    @property
    def menu_type_name(self):
        return self.__menu_type_name
        
    @property
    def menu_type_name_english(self):
        return self.__menu_type_name_english
        
    @property
    def creation_time(self):
        return self.__creation_time
        
    @property
    def store_name(self):
        return self.__store_name
        
    @property
    def store_name_english(self):
        return self.__store_name_english    
    
    @property
    def store_id(self):
        return self.__store_id
        
    @property
    def image_file(self):
        return self.__image_file
        
    @property
    def instantly(self):
        return self.__instantly
        
class order_detail_info:
    def set(self , menu_id , order_qty):
        menu = MENU.objects.get(menu_id = menu_id)
        store = STORE.objects.get(store_id = menu.store_id.store_id)
        
        self.__menu_id = menu_id
        self.__menu_name = menu.menu_name
        self.__menu_name_english = menu.menu_name_english
        self.__order_qty = order_qty
        self.__price = int(menu.price)
        self.__total_price = int(menu.price * order_qty)
        self.__store_name = store.store_name
        self.__store_id = store.store_id
        
        return self  

    @property
    def menu_id(self):
        return self.__menu_id
        
    @property
    def menu_name(self):
        return self.__menu_name
        
    @property
    def menu_name_english(self):
        return self.__menu_name_english
        
    @property
    def order_qty(self):
        return self.__order_qty
        
    @property
    def price(self):
        return self.__price
        
    @property
    def total_price(self):
        return self.__total_price
        
    @property
    def store_name(self):
        return self.__store_name
        
    @property
    def store_id(self):
        return self.__store_id
        
class store_image_list:
    def set(self , STORE, store_image_path):
        self.__store_id = STORE.store_id
        self.__store_name = STORE.store_name
        self.__store_name_english = STORE.store_name_english
        self.__store_image_path = store_image_path
        
        return self
   
    @property
    def store_id(self):
        return self.__store_id
        
    @property
    def store_name(self):
        return self.__store_name
        
    @property
    def store_name_english(self):
        return self.__store_name_english

    @property
    def store_image_path(self):
        return self.__store_image_path