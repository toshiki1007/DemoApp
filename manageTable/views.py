from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from django.utils.timezone import now
from django.template.context_processors import csrf

from .models import TABLE
from .models import RESERVE_TABLE

from .instance import tableStatus

from .consts import *

# テーブルステータス設定メソッド
def setStatus(status , table , statusList):
    if len(statusList) != 0:
        latestRecord = statusList.order_by(\
            'reservationId').reverse().first()
                
        if latestRecord.endTime != None\
            or latestRecord.cancelFlg == True:
            status.set(table,TABLE_AVAILABLE)
        else:
            status.set(table,TABLE_NOT_AVAILABLE)
    else:
        status.set(table,TABLE_AVAILABLE)
    
    return status



# テーブル一覧表示view
def table_list(request):
    tableStatusList =[]
    tableList = TABLE.objects.order_by('tableId')
    
    for table in tableList:
        status = tableStatus()
        statusList = RESERVE_TABLE.objects.\
            filter(tableId = table.tableId)
            
        status = setStatus(status , table , statusList)
        
        tableStatusList.append(status)    
    
    return render(request, 'manageTable/table_list.html',\
        {'tableStatusList': tableStatusList})
        
        
# テーブル予約確認画面view        
def confirm(request, select_tableId):
    tableStatusList =[]
    tableList = TABLE.objects.order_by('tableId')
    
    for table in tableList:
        status = tableStatus()
        statusList = RESERVE_TABLE.objects.\
            filter(tableId = table.tableId)
            
        if table.tableId == int(select_tableId):
            status.set(table,TABLE_SELECTED)
            tableStatusList.append(status)
        else:
            status = setStatus(status , table , statusList)
            
            tableStatusList.append(status)
                
    return render(request, 'manageTable/confirm.html',\
        {'tableStatusList': tableStatusList ,\
        'select_tableId': int(select_tableId)})
    
    
# テーブル予約確定view       
def reservation(request, select_tableId):
    if request.method == 'POST':
        createRecord = RESERVE_TABLE.objects.create(
                startTime = None,
                endTime = None,
                cancelFlg = False,
                tableId = TABLE.objects.get(tableId = int(select_tableId))
                )
        
        tableStatusList =[]
        tableList = TABLE.objects.order_by('tableId')
        
        for table in tableList:
            status = tableStatus()
            statusList = RESERVE_TABLE.objects.\
                filter(tableId = table.tableId)
                
            status = setStatus(status , table , statusList)
                
            tableStatusList.append(status)
        
        qrString = ORDER_URL\
            + str(createRecord.reservationId)
                
        return render(request, 'manageTable/show_qrcode.html',\
            {'qrString': qrString , 'tableStatusList': tableStatusList})
    else:
        return render(request, 'manageTable/error.html')
        
def orderPage(request, reservationId):
    return render(request, 'manageTable/order.html',\
        {'reservationId': reservationId})   
    
