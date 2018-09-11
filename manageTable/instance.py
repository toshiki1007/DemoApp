from .models import TABLE

class tableStatus:
    def set(self , TABLE , statusFlg):
        self.__tableId = TABLE.tableId
        self.__seaqty = TABLE.seaqty
        self.__status = statusFlg        
    
    @property
    def tableId(self):
        return self.__tableId
        
    @property
    def seatsNum(self):
        return self.__seaqty
        
    @property
    def status(self):
        return self.__status