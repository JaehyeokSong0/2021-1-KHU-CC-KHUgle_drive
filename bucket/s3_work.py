import boto3
import logging
import json
import os
from django.conf import settings 
from botocore.exceptions import ClientError

# BASE_DIR = settings.BASE_DIR
# MEDIA_DIR = settings.MEDIA_ROOT
s3 = boto3.client(
    's3',
    aws_access_key_id='ASIARPQAACLCQWCIP75F',
    aws_secret_access_key='JkQ3//xIrg/wqEanpAstrdD4msh4LlJ6BGYopRPW',
    aws_session_token='FwoGZXIvYXdzEIH//////////wEaDBGi5+5kN2aQr61LHyLCAQN18bvlEDvulNKxqnnyM74rFm0CSMV3FmgRg3Gean0XoSawq2gAp6CJDfXIux+cALItOyo+kCr0JrS6kdwoUOdWecaqglyPvHmxrWBdmM+PTzgdo7EEwaXp/hHHtMSAfP/hNVft8/YAprcOKb9V7VIWyCwvZ07wgKlz2VBT+k6ZQz4qtf9Uk6JOOhebEbhyX2SivJNw09u57EAyFSrnHOStwPzJ4/du9T3LLAbW2MnYemPjrxGYrVDE41NsYXSTQG0vKOLa7IUGMi1L62+WzBaIXyOmPyZuUvBpPzALpCP23RYsjW3y4DG8XvFr+kEiGRgmJxjfGoo=',
    region_name = 'us-east-1'
)

BUCKET = 'khugle-drive-admin'

def upload_file(file_name, bucket, file_path=None):
    # If S3 object_name was not specified, use file_name
    if file_path is None:
        file_path= file_name
    # Upload the fil
    response = s3.upload_file(file_name, bucket, file_path)
    return response

def list_object(bucket, folder_path, user):
    response = s3.list_objects(Bucket=bucket, Prefix=folder_path, Delimiter='/')
    file_list = []
    folder_res = response.get('CommonPrefixes')
    file_res = response.get('Contents')
    if folder_res:
        for folder in folder_res:
            file_list.append({'name': folder.get('Prefix').split('/')[-2], 'path': folder.get('Prefix'), 'is_folder': True, 'user' : user})
    if file_res:
        for file in file_res:
            file_list.append({'name': file.get('Key').split('/')[-1], 'path': file.get('Key'), 'is_folder': False, 'user':user})
    # file_list = folder_list + file_list
    return file_list


def download_file(bucket, file_path, download_path):
    response = s3.download_file(bucket, file_path, download_path)
    return response

def move_file(old_file_path, bucket, new_file_path):
    copy_source = {
        'Bucket': bucket,
        'Key' : old_file_path
    }
    s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=new_file_path)

def rename_file(old_file_path, bucket, new_file_path):  
    copy_source = {
        'Bucket': bucket,
        'Key': old_file_path
    }
    s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=new_file_path)
    s3.delete_object(Bucket=bucket, Key=old_file_path)

def delete_file(file_name, bucket):
    response = s3.delete_object(Bucket=bucket, Key=file_name)
    return response

def make_directory(dir_name, bucket, current_path):
    response = s3.put_object(Bucket=bucket, Key= current_path+dir_name+'/')
    return response

def create_bucket(bucket):
    response = s3.create_bucket(Bucket=bucket)
    return response

def update_path(path, folder):
    return path + '/' + 'folder'
