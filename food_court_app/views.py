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
from .models import STORE
from .models import STORE_CROWD

from .instance import *

from .consts import *

import boto3

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
            
        table_status_list.append(set_status(status , table , status_list))    
    
    return render(request, 'food_court_app/table_list.html',\
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
            table_status_list.append(set_status(status , table , status_list))
                
    return render(request, 'food_court_app/confirm.html',\
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
                
            table_status_list.append(set_status(status , table , status_list))
        
        qr_string = ORDER_URL\
            + str(create_record.reservation_id)
                
        return render(request, 'food_court_app/show_qrcode.html',\
            {'qr_string': qr_string , 'table_status_list': table_status_list})
    else:
        return render(request, 'food_court_app/error.html')
        
        
        
def crowd_condition(request):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('ec2-13-250-22-196.ap-southeast-1.compute.amazonaws.com')

    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')

    crowd_condition_list = []

    for store in store_list:
        store_crowd = STORE_CROWD.objects.\
            get(store_id = store.store_id)
            
        store_image_path = S3_PATH + str(store.store_id) + \
            UNDER_BAR + store.store_name + PNG
        
        crowd_condition_list.append(\
            crowd_status().set(store,store_crowd,store_image_path))

    return render(request, 'food_court_app/crowd_condition.html',\
        {'crowd_condition_list': crowd_condition_list})          
        
        
def order_page(request, reservation_id):
    return render(request, 'food_court_app/order.html',\
        {'reservation_id': reservation_id})   
    
