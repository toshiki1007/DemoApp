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

from .forms import *

import boto3
from boto3.s3.transfer import S3Transfer
import hashlib
from boto.ses.connection import SESConnection 

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

# メール送信メソッド
def send_mail(mail_address):
    conn = SESConnection()
    to_addresses = [ mail_address ]
    # SendMail APIを呼び出す
    conn.send_email( 'food_court_app_group_f@yahoo.co.jp'    # 送信元アドレス
                    ,'件名'           # メールの件名
                    ,'本文'     # メールの本文
                    ,to_addresses     # 送信先のアドレスリスト 
                    ) 




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
        
        
# 混雑状況画面表示view          
def crowd_condition(request):
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')

    crowd_condition_list = []

    for store in store_list:
        store_crowd = STORE_CROWD.objects.\
            get(store_id = store.store_id)

        file_name = str(store.image_file).split('/',1)[1]
        store_image_path = S3_PATH + file_name
        
        crowd_condition_list.append(\
            crowd_status().set(store,store_crowd,store_image_path))
            
    return render(request, 'food_court_app/crowd_condition.html',\
        {'crowd_condition_list': crowd_condition_list})          
        
#店舗追加画面表示view
def add_store_view(request):
    form = STORE_FORM()
    
    message = ""
    
    return render(request, 'food_court_app/add_store.html',\
        {'form': form , 'message': message})
        
#店舗追加view
def add_store(request):
    form = STORE_FORM()
    
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        start_date = request.POST.get('start_date')
        
        store_form = STORE_FORM(request.POST, request.FILES)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.end_date = None
            store.save()
            
            message = store.store_name + "を登録しました。"
        else:
            message = "入力に誤りがあります。"
            return render(request, 'food_court_app/add_store.html',\
                {'form': form , 'message': message})  

        new_store_crowd = STORE_CROWD.objects.create(
                store_id = store,
                wating_time = 0,
                crowd_status = 0
                )
                
        return render(request, 'food_court_app/add_store.html',\
            {'form': form , 'message': message})
    else:
        return render(request, 'food_court_app/error.html')    
        
# 注文画面表示view            
def order_page(request, reservation_id):
    menu_list = MENU.objects.filter(orderable_flg = True).\
        order_by('store_id').order_by('menu_id')
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')
    
    each_store_list = []
    
    for store in store_list:
        each_menu_list = []
        for menu in menu_list:
            if menu.store_id.store_id == store.store_id:
                #Decimal⇒intへ変換（小数点以下不要なので）
                menu.price = int(menu.price)
                
                menu_type = MENU_TYPE.objects.get(menu_type_id = menu.menu_type_id.menu_type_id)
                
                menu_store_info = menu_and_store().set(store , menu , menu_type)
                each_menu_list.append(menu_store_info)
        each_store_list.append(each_menu_list)

    order_form = ORDER_FORM()
    order_detail_form = ORDER_DETAIL_FORM()
    
    return render(request, 'food_court_app/order.html',\
        {'reservation_id': reservation_id , \
            'each_store_list': each_store_list, \
            'order_form': order_form, \
            'order_detail_form': order_detail_form})   

#注文処理view          
def order(request):
    reservation_id = request.POST.get('reservation_id')
    
    menu_id_list = request.POST.getlist('menu_id')
    order_qty_list = request.POST.getlist('order_qty')
    
    count = 0
    amount = 0
    order_detail_list = []
    
    while count < len(menu_id_list):
        menu_id = int(menu_id_list[i])
        order_qty = int(order_qty_list[i])
        
        if order_qty != 0:
            amount = amount + 1
            order_detail_list.append(order_detail_info(). \
                set(menu_id,order_qty))
                
        count = count + 1
            
    if amount != 0:
        new_order = ORDER.objects.create(
                amount = amount,
                mail = request.POST.get('mail'),
                reservation_id = RESERVE_TABLE.objects. \
                    get(reservation_id = int(reservation_id))
                )
                
        for order_detail in order_detail_list:
            new_order_detail = ORDER_DETAIL.objects.create(
                menu_id = MENU.objects. \
                    get(menu_id = int(order_detail.menu_id)),
                order_qty = order_detail.order_qty,
                order_id = new_order
                )
                
        #現状は登録済みアドレスしか送れないので、とりあえず固定値
        #send_mail(new_order.mail)
        send_mail("toshiki1007@gmail.com")
    else:
        pass

    return render(request, 'food_court_app/order_complete.html')   