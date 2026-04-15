from datetime import datetime
from sqlalchemy import create_engine, schema
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database, create_database, database_exists

from src.data_models.base_data_model import BaseDataModel
from src.data_models.user_data_model import UserDataModel
from src.data_models.posted_mail_data_model import PostedMailDataModel
from src.utils.environments import EnvironmentHelper


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:abcdef@{'database' if EnvironmentHelper.is_production() else 'localhost'}/simple_microservice"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_schema():
    create_database(engine.url)

    with engine.connect() as connection:
        connection.execute(schema.CreateSchema("admin"))
        connection.execute(schema.CreateSchema("business"))
        connection.commit()

    BaseDataModel.metadata.create_all(bind=engine)

def init_data():
    with SessionLocal() as session:
        session.add_all(
            [
                UserDataModel(
                    email="egorleontev54@gmail.com",
                    password="$2b$12$AP0NRIx9JKgC26IcYLXCy.dA/Skvp81HvkUvnKQiWzuK0gfJfF42O",
                ),
                PostedMailDataModel(
                    mail_uid="34dafd1f-86a5-4c56-9c2b-9c87cec8c2b6",
                    date=datetime.now(),
                    user_id=1,
                ),
            ]
        )

        session.commit()

def init_database():
    if EnvironmentHelper.is_production():
        if not database_exists(engine.url):
            init_schema()
    else:
        if database_exists(engine.url):
            drop_database(engine.url)

        init_schema()
        init_data()

