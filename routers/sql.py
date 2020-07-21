from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Boolean, Column, Integer, String, Text

HOST = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'apple2882960'
DB_NAME = 'fastapi'
# dialect+driver://username:password@host:port/database
DB_URI = 'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8'.format(USERNAME=USERNAME,
                                                                                             PASSWORD=PASSWORD,
                                                                                             HOST=HOST,
                                                                                             PORT=PORT, DB_NAME=DB_NAME)
SQLALCHEMY_DATEBASE_URL = DB_URI
engine = create_engine(SQLALCHEMY_DATEBASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()