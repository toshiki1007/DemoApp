import boto3

s3 = boto3.resource('s3')

bucket = s3.Bucket('toshiki1007')
bucket.download_file('available.png', 'available.png')