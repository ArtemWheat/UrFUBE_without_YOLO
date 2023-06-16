import os
from io import BytesIO
from typing import Union
from config import ENDPOINT_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, BUCKET
import typing
from fastapi import UploadFile
import aioboto3


config = {
            "service_name": 's3',
            "endpoint_url": ENDPOINT_URL,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "aws_access_key_id": AWS_ACCESS_KEY_ID
        }


async def upload_object(video: UploadFile, file: BytesIO, key: str):
    async with aioboto3.Session().client(**config) as s3:
        await s3.upload_fileobj(file, BUCKET, key, ExtraArgs={'ACL': 'public-read'})


async def remove_object(key: str):
    async with aioboto3.Session().client(**config) as s3:
        res = await s3.delete_object(Bucket=BUCKET, Key=key)
        print(res)
