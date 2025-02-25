import os
import requests
import boto3
from botocore.client import Config

from scrimmage import app

LOCAL_STORAGE_PATH = 'local_storage'

# Upload files to S3 --> when app.debug=True use local file storage

def _get_s3_context():
  # if app.debug:
  #   return boto3.client('s3', config=Config(signature_version='s3v4'))
  if app.debug:
        return None  # Indicate local storage
  else:
    return boto3.client(
      's3',
      region_name=app.config['S3_REGION'],
      aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
      aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
      config=Config(signature_version='s3v4')
    )


def get_s3_object(key):
  client = _get_s3_context()
  if client is None:
    # Local storage
    local_path = os.path.join(LOCAL_STORAGE_PATH, key)
    with open(local_path, 'rb') as f:
      return f.read()
  else:
    # S3 storage
    return client.get_object(Bucket=app.config['S3_BUCKET'], Key=key)['Body']


def put_s3_object(key, body):
  client = _get_s3_context()
  if client is None:
    # Local storage
    local_path = os.path.join(LOCAL_STORAGE_PATH, key)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, 'wb') as f:
      f.write(body.read())
  else:
    # S3 storage
    client.put_object(Body=body, Bucket=app.config['S3_BUCKET'], Key=key)


def get_student_info(kerberos):
  r = requests.get(app.config['USER_INFO_URL_BASE'], params={'user': kerberos})

  if r.status_code != 200:
    return None, None, None

  data = r.json()
  return data['name'], data['class_year'], data['department']
