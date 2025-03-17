import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-super-secreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:DG450159753@host.docker.internal:5432/estoque_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 