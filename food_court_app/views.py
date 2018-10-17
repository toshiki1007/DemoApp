from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from django.utils.timezone import now
from django.template.context_processors import csrf
from django.conf import settings

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
import stripe

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
def send_mail(mail_address, mail_title, mail_text):
    conn = SESConnection()
    to_addresses = [ mail_address ]
    # SendMail APIを呼び出す
    conn.send_email( 'food_court_app_group_f@yahoo.co.jp'    # 送信元アドレス
                    ,mail_title           # メールの件名
                    ,mail_text     # メールの本文
                    ,to_addresses     # 送信先のアドレスリスト 
                    ) 

#店舗混雑状況更新メソッド
def update_shore_crowd_status():
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')
    
    store_prospect_time_list = []
    
    for store in store_list:
        store_prospect_time = 0
        menu_list = MENU.objects.filter(store_id = store.store_id)
        
        for menu in menu_list:
            order_detail_list = ORDER_DETAIL.objects. \
                filter(menu_id = menu.menu_id). \
                filter(supply_time = None). \
                filter(cancel_flg = False)
                
            for order_detail in order_detail_list:
                #現時点の店別全オーダー処理想定時間
                #(メニュー別の調理時間*注文数の総計)
                store_prospect_time = store_prospect_time + \
                    (order_detail.order_qty * menu.creation_time)
        
        store_crowd = STORE_CROWD.objects.get(store_id = store.store_id)
        #店別の待ち時間計算処理。とりあえず10多重想定の単純計算にしておく。
        wating_time = store_prospect_time/10
        #店別の待ち時間によって混雑レベルを設定。
        #とりあえず0-5分、5-15分、15分-で区切っておく。
        if wating_time < 5:
            store_crowd.crowd_status = CROWD_LEVEL_1
        elif wating_time < 15:
            store_crowd.crowd_status = CROWD_LEVEL_2
        else:
            store_crowd.crowd_status = CROWD_LEVEL_3
        
        store_crowd.wating_time = wating_time
           
        store_crowd.save()

#メニュー一覧作成メソッド
def create_menu_list(request):
    reservation_id = request.POST.get('reservation_id')    
    store_id = request.POST.get('store_id')  
    
    store = STORE.objects.get(store_id = store_id)
    menu_list = MENU.objects. \
        filter(store_id = store). \
        filter(orderable_flg = True).order_by('menu_id')
        
    for menu in menu_list:
        file_name = str(menu.image_file).split('/',1)[1]
        store_image_path = S3_PATH + file_name
        
        menu.price = int(menu.price)
        menu.image_file = store_image_path
        
    return reservation_id,store, menu_list

#全店舗分メニュー一覧作成メソッド
def create_menu_list_all_store():
    menu_list = MENU.objects.filter(orderable_flg = True).\
        order_by('store_id').order_by('menu_id')
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')
    
    each_store_list = []
    
    for store in store_list:
        each_menu_list = []
        for menu in menu_list:
            if menu.store_id.store_id == store.store_id:
                file_name = str(menu.image_file).split('/',1)[1]
                store_image_path = S3_PATH + file_name
                
                menu.price = int(menu.price)
                menu.image_file = store_image_path
                
                menu_type = MENU_TYPE.objects.get(menu_type_id = menu.menu_type_id.menu_type_id)
                
                menu_store_info = menu_and_store().set(store , menu , menu_type)
                each_menu_list.append(menu_store_info)

        each_store_list.append(each_menu_list)
        
    return each_store_list

#店舗別注文管理情報取得メソッド
def get_order_info(select_store_id):
    store_name = STORE.objects.get(store_id=select_store_id).store_name
    
    order_detail_list = ORDER_DETAIL.objects.select_related(). \
        filter(menu_id_id__store_id=select_store_id). \
        filter(order_id_id__status=0). \
        order_by('order_id')
        
    return store_name, order_detail_list

#注文状況更新メソッド
def update_order_status(order_detail_id):
    order_id = ORDER_DETAIL.objects. \
        filter(order_detail_id = order_detail_id)[0].order_id
        
    order_detail_list = ORDER_DETAIL.objects. \
        filter(order_id = order_id)
        
    order_status_update_flg = True
    for order_detail in order_detail_list:
        if order_detail.cancel_flg != True and \
          order_detail.supply_time == None:
                order_status_update_flg = False
                break
            
    if order_status_update_flg:
        order = ORDER.objects.get(order_id = order_id.order_id)
        order.status = 1
        order.save()
        


# テーブル一覧表示view
def table_list(request):
    table_status_list =[]
    table_list = TABLE.objects.order_by('table_id')
    
    for table in table_list:
        status = table_status()
        status_list = RESERVE_TABLE.objects.\
            filter(table_id = table.table_id)
            
        table_status_list.append(set_status(status , table , status_list))   
        
    update_shore_crowd_status()
    
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
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')
        
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
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')    

    form = STORE_FORM()

    store_name = request.POST.get('store_name')
    start_date = request.POST.get('start_date')
    
    store_form = STORE_FORM(request.POST, request.FILES)
    if store_form.is_valid():
        store = store_form.save(commit=False)
        store.end_date = None
        store.save()
        
        message = store.store_name + "を登録しました。"
    else:
        message = INPUT_ERROR_MESSAGE
        return render(request, 'food_court_app/add_store.html',\
            {'form': form , 'message': message})  

        new_store_crowd = STORE_CROWD.objects.create(
            store_id = store,
            wating_time = 0,
            crowd_status = 0
            )
                
    return render(request, 'food_court_app/add_store.html',\
        {'form': form , 'message': message})

#注文用店舗選択画面view
def select_store_for_order(request, reservation_id):
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')    
        
    show_store_list = []

    for store in store_list:
        file_name = str(store.image_file).split('/',1)[1]
        store_image_path = S3_PATH + file_name
        
        show_store_list.append(\
            store_image_list().set(store,store_image_path))

    return render(request, 'food_court_app/select_store_for_order.html', \
            {'show_store_list': show_store_list, \
                'reservation_id': reservation_id })   
        
# 注文画面表示view            
def order_page(request):
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')  

    reservation_id, store, menu_list = create_menu_list(request)
        
    order_form = ORDER_FORM()
    order_detail_form = ORDER_DETAIL_FORM()
    
    message = ""
    
    return render(request, 'food_court_app/order.html',\
        {'reservation_id': reservation_id , \
            'store': store, \
            'menu_list': menu_list, \
            'message': message, \
            'order_form': order_form, \
            'order_detail_form': order_detail_form})  
            
# 注文画面表示(全店舗)view   
def order_page_all_store(request,reservation_id):
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')    
        
    show_store_list = []

    for store in store_list:
        file_name = str(store.image_file).split('/',1)[1]
        store_image_path = S3_PATH + file_name
        
        show_store_list.append(\
            store_image_list().set(store,store_image_path))
            
    each_store_list = create_menu_list_all_store()

    order_form = ORDER_FORM()
    order_detail_form = ORDER_DETAIL_FORM()
    
    message = ""
    
    return render(request, 'food_court_app/order_all_store.html',\
        {'reservation_id': reservation_id , \
            'message': message, \
            'each_store_list': each_store_list, \
            'show_store_list': show_store_list, \
            'order_form': order_form, \
            'order_detail_form': order_detail_form})

#注文確認View
def order_confirm(request):
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')      
    
    reservation_id = request.POST.get('reservation_id')
    select_store_flg = request.POST.get('select_store_flg')
    
    if select_store_flg == "True":
        store_name = request.POST.get('store_name')
    else:
        store_name = "全店舗"
    
    menu_id_list = request.POST.getlist('menu_id')
    order_qty_list = request.POST.getlist('order_qty')
    mail = request.POST.get('mail')
    
    #カウント処理用
    count = 0
    list_count = 0
    #注文数総計
    amount = 0
    #画面表示用の総計金額
    total_price = 0
    
    order_detail_list = []
    
    while count < len(menu_id_list):
        menu_id = int(menu_id_list[count])
        order_qty = int(order_qty_list[count])
        
        if order_qty > 0:
            order_detail_list.append(order_detail_info(). \
                set(menu_id,order_qty))
            total_price = total_price + order_detail_list[list_count].total_price
            list_count = list_count + 1
            amount = amount + order_qty
            
        count = count + 1
         
    #注文数が1件以上無い場合はエラー   
    if amount < 1:
        order_form = ORDER_FORM()
        order_detail_form = ORDER_DETAIL_FORM()
        
        message = AMOUNT_ERROR_MESSAGE
    
        if select_store_flg == True:
            reservation_id, store, menu_list = create_menu_list(request)
            
            return render(request, 'food_court_app/order.html',\
                {'reservation_id': reservation_id , \
                    'store': store, \
                    'menu_list': menu_list, \
                    'message': message, \
                    'order_form': order_form, \
                    'order_detail_form': order_detail_form}) 
        else:
            store_list = STORE.objects.filter(end_date = None).\
                order_by('store_id')    
        
            show_store_list = []
        
            for store in store_list:
                file_name = str(store.image_file).split('/',1)[1]
                store_image_path = S3_PATH + file_name
                
                show_store_list.append(\
                    store_image_list().set(store,store_image_path))
                    
            each_store_list = create_menu_list_all_store()
    
            return render(request, 'food_court_app/order_all_store.html',\
                {'reservation_id': reservation_id , \
                    'message': message, \
                    'each_store_list': each_store_list, \
                    'show_store_list': show_store_list, \
                    'order_form': order_form, \
                    'order_detail_form': order_detail_form})
 
    publick_key = settings.STRIPE_PUBLIC_KEY

    return render(request, 'food_court_app/order_confirm.html',\
        {'reservation_id': reservation_id , \
            'store_name': store_name , \
            'mail': mail , \
            'amount': amount , \
            'select_store_flg': select_store_flg , \
            'total_price': total_price , \
            'publick_key': publick_key , \
            'order_detail_list': order_detail_list})   

#注文処理view          
def order(request):
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')  
        
    store_name = request.POST.get('store_name')
    reservation_id = request.POST.get('reservation_id')
    mail = request.POST.get('mail')
    amount = request.POST.get('amount')
    total_price = request.POST.get('total_price')
    menu_id_list = request.POST.getlist('menu_id')
    order_qty_list = request.POST.getlist('order_qty')

    order_detail_list = []
    count = 0
    
    while count < len(menu_id_list):
        menu_id = int(menu_id_list[count])
        order_qty = int(order_qty_list[count])
        
        order_detail_list.append(order_detail_info(). \
            set(menu_id,order_qty))
            
        count = count + 1
    
    reserve_table = RESERVE_TABLE.objects.get( \
        reservation_id = int(reservation_id))

    stripe.api_key = settings.STRIPE_SECRET_KEY
    token = request.POST['stripeToken']

    try:
        #注文レコード登録
        new_order = ORDER.objects.create(
                amount = amount,
                mail = request.POST.get('mail'),
                reservation_id = reserve_table
                )
        #注文明細レコード登録        
        for order_detail in order_detail_list:
            new_order_detail = ORDER_DETAIL.objects.create(
            menu_id = MENU.objects. \
                get(menu_id = int(order_detail.menu_id)),
                order_qty = order_detail.order_qty,
                order_id = new_order
                )   
        #テーブル予約レコード更新
        reserve_table.start_time = datetime.now()
        reserve_table.save()
        #決済処理 
        charge = stripe.Charge.create(
            amount=total_price, 
            currency='jpy',
            source=token,
            description= \
                '店舗：' + store_name + \
                ' , 注文番号：' + str(new_order.order_id),
        )
    except stripe.error.CardError as e:
        return render(request, 'food_court_app/payment_error.html', {
            'message': "Your payment cannot be completed. The card has been declined.",
        }) 

            
    #現状は登録済みアドレスしか送れないので、とりあえず固定値
    #send_mail(new_order.mail,"メール件名" ,"メール本文")
    send_mail("food_court_app_group_f@yahoo.co.jp","注文を受け付けました。" , \
        "注文を受け付けました。")
    
    #店舗別の混雑状況を更新
    update_shore_crowd_status()

    return render(request, 'food_court_app/order_complete.html', \
            {'mail': new_order.mail})      


#店舗選択画面view
def select_store(request):
    store_list = STORE.objects.filter(end_date = None).\
        order_by('store_id')    

    return render(request, 'food_court_app/select_store.html', \
            {'store_list': store_list})   
    
#オーダー管理画面表示view
def manage_order_view(request):
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')      

    select_store_id = request.POST.get('select_store_id')
    
    store_name, order_detail_list = get_order_info(select_store_id)
        
    return render(request, 'food_court_app/manage_order.html', \
            {'order_detail_list': order_detail_list, \
            'store_name': store_name, \
            'select_store_id': select_store_id})   
            
#料理提供view
def order_supply(request):
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')      
    
    order_detail_id = request.POST.get('order_detail_id')
    select_store_id = request.POST.get('select_store_id')
    
    #提供済処理
    order_detail = ORDER_DETAIL.objects.get(order_detail_id=order_detail_id)
    order_detail.supply_time = datetime.now()
    order_detail.save()
    
    store_name, order_detail_list = get_order_info(select_store_id)

    #現状は登録済みアドレスしか送れないので、とりあえず固定値
    #send_mail(new_order.mail,"メール件名" ,"メール本文")
    send_mail("food_court_app_group_f@yahoo.co.jp","ご注文の料理が出来上がりました。" , \
        store_name + "までお越しください。")
    
    update_order_status(order_detail_id)
    update_shore_crowd_status()
        
    return render(request, 'food_court_app/manage_order.html', \
            {'order_detail_list': order_detail_list, \
            'store_name': store_name, \
            'select_store_id': select_store_id})  
            
#注文キャンセルview
def order_cancel(request):
    if request.method != 'POST':
        return render(request, 'food_court_app/error.html')      
    
    order_detail_id = request.POST.get('order_detail_id')
    select_store_id = request.POST.get('select_store_id')
    
    #注文取消処理
    order_detail = ORDER_DETAIL.objects.get(order_detail_id=order_detail_id)
    order_detail.cancel_flg = True
    order_detail.save()
    
    store_name, order_detail_list = get_order_info(select_store_id)

    #現状は登録済みアドレスしか送れないので、とりあえず固定値
    #send_mail(new_order.mail,"メール件名" ,"メール本文")
    send_mail("food_court_app_group_f@yahoo.co.jp","ご注文をキャンセルしました。" , \
        "ご注文をキャンセルしました。")
    
    update_order_status(order_detail_id)
    update_shore_crowd_status()
        
    return render(request, 'food_court_app/manage_order.html', \
            {'order_detail_list': order_detail_list, \
            'store_name': store_name, \
            'select_store_id': select_store_id})   