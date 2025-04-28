from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import logging

DATABASE_URL = "postgresql+asyncpg://postgres:adminpassword@localhost:5432/housing_service"
engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_session() as session:
        yield session

async def setup_database():
    from src.models.users import Role, UserModel

    async with engine.begin() as conn:
        logging.info("Dropping existing tables...")
        await conn.run_sync(Base.metadata.drop_all)
        logging.info("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)

    async with new_session() as session:
        existing_users = await session.execute(select(UserModel))
        if existing_users.scalars().first() is None:
            dispatcher = UserModel(username="Vira", password="1234", role=Role.DISPATCHER)
            householder = UserModel(username="Ostap", password="abcd", role=Role.HOUSEHOLDER)
            session.add_all([dispatcher, householder])
            await session.commit()
            logging.info("Default users created")
