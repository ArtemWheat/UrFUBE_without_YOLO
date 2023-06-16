from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT_URL = os.environ['ENDPOINT_URL']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
BUCKET = os.environ['BUCKET']
SECRET_PASSWORDS = os.environ['SECRET_PASSWORDS']
DATABASE_URL = os.environ['DATABASE_URL']
MAX_UPLOAD_SIZE = int(os.environ['MAX_UPLOAD_SIZE'])