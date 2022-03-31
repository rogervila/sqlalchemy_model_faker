import unittest
from random import randint
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy_model_faker import factory


class Product(declarative_base()):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    price = Column(Integer)


class test_factory(unittest.TestCase):
    engine = None  # type: engine.base.Engine
    session = None  # type: Session

    def test_column_data_types(self):
        product = factory(Product).make()
        self.assertIsInstance(product.description, str)
        self.assertIsInstance(product.price, int)

    def test_factory_creates_model(self):
        self._prepare_database()

        amount = randint(1, 10)

        with self.session() as session:
            for _ in range(amount):
                product = factory(Product).make()  # type: Product
                session.add(product)
                session.commit()

        with self.session() as session:
            results = session.query(Product).all()
            self.assertEqual(len(results), amount)

    def test_model_persisted_with_specified_data(self):
        self._prepare_database()

        integer_value = randint(42, 288)
        text_value = 'lorem ipsum dolor sit amet'

        with self.session() as session:
            product = factory(Product).make({
                'price': integer_value,
                'description': text_value
            })  # type: Product
            session.add(product)
            session.commit()

        with self.session() as session:
            product = session.query(Product).first()  # type: Product
            self.assertEqual(product.price, integer_value)
            self.assertEqual(product.description, text_value)

    def test_autoincremental_values_return_as_none(self):
        product = factory(Product).make()
        self.assertIsNone(product.id)

    def test_autoincremental_values_return_specified_value(self):
        id_value = randint(42, 288)
        product = factory(Product).make({
            'id': id_value
        })
        self.assertEqual(product.id, id_value)

    def test_ignored_columns(self):
        product = factory(Product).make(ignored_columns=['price'])
        self.assertIsNone(product.price)

    def _prepare_database(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(bind=self.engine)

        with self.engine.begin() as connection:
            connection.execute('''
                CREATE TABLE products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    price INTEGER
                )
            ''')


if __name__ == '__main__':
    unittest.main()
