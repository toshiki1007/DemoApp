from .models import TABLE

class table_status:
    def set(self , TABLE , status_flg):
        self.__table_id = TABLE.table_id
        self.__seat_qty = TABLE.seat_qty
        self.__status = status_flg        
    
    @property
    def table_id(self):
        return self.__table_id
        
    @property
    def seat_qty(self):
        return self.__seat_qty
        
    @property
    def status(self):
        return self.__status