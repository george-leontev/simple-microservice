from datetime import datetime
from sqlalchemy import create_engine, schema
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database, create_database, database_exists

from src.data_models.base_data_model import BaseDataModel
from src.data_models.user_data_model import UserDataModel
from src.data_models.posted_mail_data_model import PostedMailDataModel
from src.utils.environments import is_production


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:abcdef@{'database' if is_production() else 'localhost'}/simple_microservice"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_schema():
    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)

    with engine.connect() as connection:
        connection.execute(schema.CreateSchema('admin'))
        connection.execute(schema.CreateSchema('business'))
        connection.commit()

    BaseDataModel.metadata.create_all(bind=engine)

def init_data():
    with SessionLocal() as session:
        session.add_all([
            UserDataModel(
                email='egorleontev54@gmail.com',
                password='bef57ec7f53a6d40beb640a780a639c83bc29ac8a9816f1fc6c5c6dcd93c4721'
            ),
            PostedMailDataModel(
                mail_uid='34dafd1f-86a5-4c56-9c2b-9c87cec8c2b6',
                date=datetime.now(),
                user_id=1
            )
        ])

        session.commit()
