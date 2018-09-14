from .models import TABLE,STORE,STORE_CROWD
import boto3

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