from Cinescope.resources.db_creds import PostgresCreds
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker



connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=PostgresCreds.USERNAME,
        password=PostgresCreds.PASSWORD,
        host=PostgresCreds.HOST,
        port=PostgresCreds.PORT,
        database=PostgresCreds.NAME,
    )

engine = create_engine(connection_url)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

def check_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Соединение с PostgreSQL установлено")
    except Exception as error:
        print(f"Ошибка подключения к PostgreSQL: {error}")

def get_db_session():
    return SessionLocal()
