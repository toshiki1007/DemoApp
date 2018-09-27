import os

HOME_URL = "http://ec2-52-194-11-29.ap-northeast-1."\
            + "compute.amazonaws.com/"
            
ORDER_URL = HOME_URL + "select_store_for_order/"
S3 = "s3"

#本番用
S3_PATH = "https://s3-ap-northeast-1.amazonaws.com/"\
    +"ec2-52-194-11-29.ap-northeast-1.compute.amazonaws.com/"
S3_BUCKET_NAME = "ec2-52-194-11-29.ap-northeast-1.compute.amazonaws.com"    

#開発環境用
#S3_PATH = "https://s3-ap-southeast-1.amazonaws.com/"\
#    +"groupf-test-bucket/"
#S3_BUCKET_NAME = "groupf-test-bucket"    

PNG = ".png"
UNDER_BAR = "_"

TABLE_AVAILABLE = 0
TABLE_NOT_AVAILABLE = 1
TABLE_SELECTED = 2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INPUT_ERROR_MESSAGE = "入力に誤りがあります。"
AMOUNT_ERROR_MESSAGE = "注文数が0件です。"

CROWD_LEVEL_1 = 0
CROWD_LEVEL_2 = 1
CROWD_LEVEL_3 = 2