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

from .instance import table_status

from .consts import *

# テーブルステータス設定メソッド
def set_status(status , table , status_list):
    if len(status_list) != 0:
        latest_record = status_list.order_by(\
            'reservation_id').reverse().first()
                
        if latest_record.end_time != None\
            or latest_record.cancel_flg == True:
            status.set(table,TABLE_AVAILABLE)
        else:
            status.set(table,TABLE_NOT_AVAILABLE)
    else:
        status.set(table,TABLE_AVAILABLE)
    
    return status



# テーブル一覧表示view
def table_list(request):
    table_status_list =[]
    table_list = TABLE.objects.order_by('table_id')
    
    for table in table_list:
        status = table_status()
        status_list = RESERVE_TABLE.objects.\
            filter(table_id = table.table_id)
            
        status = set_status(status , table , status_list)
        
        table_status_list.append(status)    
    
    return render(request, 'manageTable/table_list.html',\
        {'table_status_list': table_status_list})
        
        
# テーブル予約確認画面view        
def confirm(request, select_table_id):
    table_status_list =[]
    table_list = TABLE.objects.order_by('table_id')
    
    for table in table_list:
        status = table_status()
        status_list = RESERVE_TABLE.objects.\
            filter(table_id = table.table_id)
            
        if table.table_id == int(select_table_id):
            status.set(table,TABLE_SELECTED)
            table_status_list.append(status)
        else:
            status = set_status(status , table , status_list)
            
            table_status_list.append(status)
                
    return render(request, 'manageTable/confirm.html',\
        {'table_status_list': table_status_list ,\
        'select_table_id': int(select_table_id)})
    
    
# テーブル予約確定view       
def reservation(request, select_table_id):
    if request.method == 'POST':
        create_record = RESERVE_TABLE.objects.create(
                start_time = None,
                end_time = None,
                cancel_flg = False,
                table_id = TABLE.objects.get(table_id = int(select_table_id))
                )
        
        table_status_list =[]
        table_list = TABLE.objects.order_by('table_id')
        
        for table in table_list:
            status = table_status()
            status_list = RESERVE_TABLE.objects.\
                filter(table_id = table.table_id)
                
            status = set_status(status , table , status_list)
                
            table_status_list.append(status)
        
        qr_string = ORDER_URL\
            + str(create_record.reservation_id)
                
        return render(request, 'manageTable/show_qrcode.html',\
            {'qr_string': qr_string , 'table_status_list': table_status_list})
    else:
        return render(request, 'manageTable/error.html')
        
def order_page(request, reservation_id):
    return render(request, 'manageTable/order.html',\
        {'reservation_id': reservation_id})   
    
