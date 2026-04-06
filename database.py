from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})#DB本体との接続設定
                       
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#DB操作用の「セッション工場」

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()