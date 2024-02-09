import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from configparser import ConfigParser
import json
from models import create_tables, Publisher, Book, Shop, Stock, Sale

config = ConfigParser()
config.read('config.ini')
engine = sq.create_engine(config['Settings']['DSN'])

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Задание 3

with open('tests_data.json') as data_file:
    data = json.load(data_file)
models = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }
for record in data:
    model = models[record.get('model')]
    session.add(model(**record.get('fields')))
session.commit()

# Задание 2

p_name = input('Введите название издателя: ')

q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
    .join(Publisher, Publisher.id == Book.id_publisher) \
    .join(Stock, Stock.id_book == Book.id) \
    .join(Shop, Shop.id == Stock.id_shop) \
    .join(Sale, Sale.id_stock == Stock.id) \
    .filter(Publisher.name == p_name)
for record in q.all():
    print(f"{record[0]:<40} | {record[1]:<10} | {record[2]:<5} | {record[3]:%Y-%m-%d}")

session.close()