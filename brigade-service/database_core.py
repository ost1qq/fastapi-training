import logging
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select
from datetime import datetime
import sys

DATABASE_URL = "postgresql+asyncpg://postgres:adminpassword@postgres-microservices:5432/brigades"

async def connect_create_if_not_exists(user, database, password, host):
    try:
        conn = await asyncpg.connect(
            database=database, user=user, password=password, host=host
        )
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(user=user, password=password, host=host)
        await sys_conn.execute(f'CREATE DATABASE "{database}" OWNER "{user}"')
        await sys_conn.close()
        conn = await asyncpg.connect(
            user=user, password=password, host=host, database=database
        )
    return conn

engine = create_async_engine(DATABASE_URL, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_session() as session:
        yield session

async def setup_database():
    from models.brigade import Brigade

    await connect_create_if_not_exists(
        user="postgres",
        password="adminpassword",
        database="brigades",
        host="postgres-microservices",
    )

    async with engine.begin() as conn:
        logging.info("Creating brigade-service tables...")
        await conn.run_sync(Base.metadata.create_all)
