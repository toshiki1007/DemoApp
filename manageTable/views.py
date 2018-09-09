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
from .models import TABLE_STATUS

from .instance import tableStatus

# テーブルステータス設定メソッド
def setStatus(status , table , statusList):
    if len(statusList) != 0:
        latestRecord = statusList.order_by(\
            'reservationId').reverse().first()
                
        if latestRecord.endDateTime != None\
            or latestRecord.cancelFlg == True:
            status.set(table,'0')
        else:
            status.set(table,'1')
    else:
        status.set(table,'0')
    
    return status



# テーブル一覧表示view
def table_list(request):
    tableStatusList =[]
    tableList = TABLE.objects.filter(areaId = 1).order_by('tableId')
    
    for table in tableList:
        status = tableStatus()
        statusList = TABLE_STATUS.objects.\
            filter(tableId = table.tableId)
            
        status = setStatus(status , table , statusList)
        
        tableStatusList.append(status)    
    
    return render(request, 'manageTable/table_list.html',\
        {'tableStatusList': tableStatusList})
        
        
# テーブル予約確認画面view        
def confirm(request, select_tableId):
    tableStatusList =[]
    tableList = TABLE.objects.filter(areaId = 1).order_by('tableId')
    
    for table in tableList:
        status = tableStatus()
        statusList = TABLE_STATUS.objects.\
            filter(tableId = table.tableId)
            
        if table.tableId == int(select_tableId):
            status.set(table,'2')
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
        latestRecord = TABLE_STATUS.objects.order_by('reservationId')\
             .reverse().first();
        
        id = 0
        if latestRecord != None:
            id = latestRecord.reservationId    

        createRecord = TABLE_STATUS.objects.create(
                reservationId = id + 1,
                reservationDateTime = timezone.now(),
                startDateTime = None,
                endDateTime = None,
                cancelFlg = False,
                tableId = TABLE.objects.get(tableId = int(select_tableId))
                )
        
        tableStatusList =[]
        tableList = TABLE.objects.filter(areaId = 1).order_by('tableId')
        
        for table in tableList:
            status = tableStatus()
            statusList = TABLE_STATUS.objects.\
                filter(tableId = table.tableId)
                
            status = setStatus(status , table , statusList)
                
            tableStatusList.append(status)
        
        qrString = "http://ec2-52-77-80-183.ap-southeast-1."\
            + "compute.amazonaws.com/orderPage/"\
            + str(createRecord.reservationId)
                
        return render(request, 'manageTable/show_qrcode.html',\
            {'qrString': qrString , 'tableStatusList': tableStatusList})
    else:
        return redirect('/')
        
def orderPage(request, reservationId):
    return render(request, 'manageTable/order.html',\
        {'reservationId': reservationId})   
    
