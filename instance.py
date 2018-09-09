from .models import TABLE

class tableStatus:
    def set(self , TABLE , statusFlg):
        self.tableId = TABLE.tableId
        self.seatsNum = TABLE.seatsNum
        self.areaId = TABLE.areaId
        self.status = statusFlg
    
        return self