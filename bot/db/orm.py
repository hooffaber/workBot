from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Worker
from bot.config_reader import load_config

config = load_config()
db_name = config.db.db_name

db_url = f'sqlite:///{db_name}.db'
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_user(tg_name: str, fullname: str):
    session = Session()
    user = session.query(Worker).filter(Worker.tg_name == tg_name).first()
    if not user:
        new_worker = Worker(tg_name=tg_name, fullname=fullname)
        session.add(new_worker)
        session.commit()



