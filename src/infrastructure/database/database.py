from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.infrastructure.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    pool_size=settings.MAX_CONNECTIONS,
    max_overflow=20,
    pool_timeout=30,
    echo=False,
)



AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    future=True,
    
)
Base = declarative_base()

@asynccontextmanager
async def get_db() :
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()
