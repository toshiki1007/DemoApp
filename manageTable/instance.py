from .models import TABLE

class tableStatus:
    def set(self , TABLE , statusFlg):
        self.__tableId = TABLE.tableId
        self.__seatsNum = TABLE.seatsNum
        self.__areaId = TABLE.areaId
        self.__status = statusFlg        
    
    @property
    def tableId(self):
        return self.__tableId
        
    @property
    def seatsNum(self):
        return self.__seatsNum
        
    @property
    def areaId(self):
        return self.__areaId
        
    @property
    def status(self):
        return self.__status