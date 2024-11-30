from sqlmodel import SQLModel, create_engine, Session


sqlite_filename = "database/database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def conn():
    SQLModel.metadata.create_all(engine)


def drop_database():
    SQLModel.metadata.drop_all(engine)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
