from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL ma'lumotlar bazasi bilan ulanish
engine = create_engine('postgresql+psycopg2://nizom:nizom@localhost:5432/medium_db', echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)

class Template(Base):
    __tablename__ = 'taxy_shablon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)

class Customers(Base):
    __tablename__ = 'yaypan_taxi_bot'
    chat_id = Column(Integer, primary_key=True)
    chat_type = Column(String)

class Customers2(Base):
    __tablename__ = 'yaypan_taxi_bot_group_new'
    chat_id = Column(String, primary_key=True)
    title = Column(String)

class Customers3(Base):
    __tablename__ = 'yaypan_taxi_bot_send_users'
    chat_id = Column(String, primary_key=True)

Base.metadata.create_all(engine)

# Yangi sessiya olish va uni yopish uchun yordamchi funksiya
def get_session():
    session = Session()
    try:
        return session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

async def create_template(context):
    session = get_session()
    try:
        # Eski template'larni o'chirish
        session.query(Template).delete()
        template = Template(content=context)
        session.add(template)
        session.commit()
    finally:
        session.close()

async def get_template():
    session = get_session()
    try:
        return session.query(Template).first()
    finally:
        session.close()

async def send_users_add(chat_id):
    session = get_session()
    try:
        customer = Customers3(chat_id=chat_id)
        session.add(customer)
        session.commit()
    finally:
        session.close()

async def del_admin_user(chat_id):
    session = get_session()
    try:
        user = session.query(Customers3).filter(Customers3.chat_id==str(chat_id)).first()
        session.delete(user)
        session.commit()
    finally:
        session.close()

async def get_user(chat_id):
    session = get_session()
    try:
        result = session.query(Customers3).filter(Customers3.chat_id == str(chat_id)).first()
        return result
    finally:
        session.close()

async def new_user_add(chat_id, chat_type):
    session = get_session()
    try:
        customer = Customers(chat_id=chat_id, chat_type=chat_type)
        session.add(customer)
        session.commit()
    finally:
        session.close()

async def new_group_add(chat_id, title):
    session = get_session()
    try:
        session.query(Customers2).delete()
        group = Customers2(chat_id=chat_id, title=title)
        session.add(group)
        session.commit()
    finally:
        session.close()

async def get_group():
    session = get_session()
    try:
        result = session.query(Customers2).first()
        return result
    finally:
        session.close()

async def getUserList(chat_type):
    session = get_session()
    try:
        result = session.query(Customers).filter(Customers.chat_type == chat_type).all()
        return result
    finally:
        session.close()

async def getUsersCount(chat_type):
    session = get_session()
    try:
        result = session.query(Customers).filter(Customers.chat_type == chat_type).count()
        return result
    finally:
        session.close()

async def getUserId(user_id):
    session = get_session()
    try:
        result = session.query(Customers).filter(Customers.chat_id == user_id).first()
        return result
    finally:
        session.close()
