import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_bookshop import create_tables, Book, Publisher, Shop, Stock, Sale

db = # база данных
name_ = 'postgres'
key_ = # пароль

dsn = 'postgresql://' + name_ + ':' + key_ + '@localhost:5432/' + db
engine = sqlalchemy.create_engine(dsn)



# Функция загрузки данных в таблицы
def add_dataset() :
    with open('tests_data.json', 'r') as f :
        data_list = json.load(f)

    #сессия
    Session = sessionmaker(bind=engine)
    session = Session()

    for one in data_list :
        
        if one['model'] == 'publisher' :
            add_data = Publisher(id=one['pk'], name = one['fields']['name'])
            session.add(add_data)
        
        elif one['model'] == 'book' :
            add_data = Book(id=one['pk'], title = one['fields']['title'], id_publisher = one['fields']['id_publisher'])
            session.add(add_data)
    
        elif one['model'] == 'shop' :
            add_data = Shop(id=one['pk'], name = one['fields']['name'])
            session.add(add_data)

        elif one['model'] == 'stock' :
            add_data = Stock(id=one['pk'], id_book = one['fields']['id_book'], id_shop = one['fields']['id_shop'], count = one['fields']['count'])
            session.add(add_data)
        
        elif one['model'] == 'sale' :
            add_data = Sale(id=one['pk'], price = one['fields']['price'], date_sale = one['fields']['date_sale'], id_stock = one['fields']['id_stock'], count = one['fields']['count'])
            session.add(add_data)

    session.commit()
    session.close()
# функция поиска книг по автору
def search_books() :
    Session = sessionmaker(bind=engine)
    session = Session()

    author_name = input('Введите имя автора : ')
    subq = session.query(Publisher.id).filter(Publisher.name == author_name).subquery()
    sq = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Stock.book_s).join(Stock.shop_s).join(Sale).join(subq, Book.id_publisher == subq.c.id).all()

    print()
    for i in sq :
        for i2 in i :
            print(i2, end=' | ')
        print()


# Проверяем работу функций
create_tables(engine)
add_dataset()
search_books()