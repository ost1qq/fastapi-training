import asyncio
import logging

import asyncpg

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import database_exists, create_database

DATABASE_URL = "postgresql+asyncpg://postgres:adminpassword@postgres:5432/householder"


async def connect_create_if_not_exists(user, database, password, host):
    try:
        conn = await asyncpg.connect(
            database=database, user=user, password=password, host=host
        )
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(user=user, password=password, host=host)
        await sys_conn.execute(f'CREATE DATABASE "{database}" OWNER "{user}"')
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(
            user=user, password=password, host=host, database=database
        )

    return conn


engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with new_session() as session:
        yield session


async def setup_database():

    await connect_create_if_not_exists(
        user="postgres",
        password="adminpassword",
        database="householder",
        host="postgres",
    )

    async with engine.begin() as conn:
        logging.info("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)
