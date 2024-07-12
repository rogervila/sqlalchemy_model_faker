import unittest
from datetime import datetime, date, time
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, engine, Column, BigInteger, Boolean, Date, DateTime, Float, Integer, Numeric, \
    SmallInteger, String, Text, Time, text
from faker import Faker
from sqlalchemy_model_faker import factory

FIELD_LENGTH = 13


class Product(declarative_base()):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    short_name = Column(String(FIELD_LENGTH))
    description = Column(Text)
    price = Column(Integer)
    total_sells = Column(BigInteger)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    promotion_day = Column(Date)
    promotion_hour = Column(Time)
    last_day_updates = Column(SmallInteger)
    total_units = Column(Numeric)
    rate = Column(Float)


class test_factory(unittest.TestCase):
    engine = None  # type: engine.base.Engine
    session = None  # type: Session
    faker = Faker()  # type: Faker

    def test_column_data_types(self):
        product = factory(Product).make()
        self.assertIsNone(product.id)
        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.short_name, str)
        self.assertIsInstance(product.description, str)
        self.assertIsInstance(product.price, int)
        self.assertIsInstance(product.total_sells, int)
        self.assertIsInstance(product.is_active, bool)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsInstance(product.promotion_day, date)
        self.assertIsInstance(product.promotion_hour, time)
        self.assertIsInstance(product.last_day_updates, int)
        self.assertIsInstance(product.total_units, float)
        self.assertIsInstance(product.rate, float)

    def test_factory_creates_model(self):
        self._prepare_database()

        amount = self.faker.random_int(min=0, max=10)

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

        integer_value = self.faker.random_int(min=42, max=288)
        string_value = 'leverage'
        text_value = 'lorem ipsum dolor sit amet'
        bigint_value = self.faker.random_int(min=10000, max=100000)
        boolean_value = self.faker.boolean()
        datetime_value = datetime.now()
        date_value = datetime_value.date()
        time_value = datetime_value.time()
        smallint_value = self.faker.random_int(min=0, max=1)
        float_value = float(self.faker.random_int(min=42, max=288))

        with self.session() as session:
            product = factory(Product).make({
                'price': integer_value,
                'name': string_value,
                'short_name': string_value,
                'description': text_value,
                'total_sells': bigint_value,
                'is_active': boolean_value,
                'created_at': datetime_value,
                'promotion_day': date_value,
                'promotion_hour': time_value,
                'last_day_updates': smallint_value,
                'total_units': float_value,
                'rate': float_value,
            })  # type: Product
            session.add(product)
            session.commit()

        with self.session() as session:
            product = session.query(Product).first()  # type: Product | None
            self.assertIsNotNone(product)
            self.assertEqual(product.price, integer_value)
            self.assertEqual(product.name, string_value)
            self.assertEqual(product.short_name, string_value)
            self.assertEqual(product.description, text_value)
            self.assertEqual(product.total_sells, bigint_value)
            self.assertEqual(product.is_active, boolean_value)
            self.assertEqual(product.created_at, datetime_value)
            self.assertEqual(product.promotion_day, date_value)
            self.assertEqual(product.promotion_hour, time_value)
            self.assertEqual(product.last_day_updates, smallint_value)
            self.assertEqual(product.total_units, float_value)
            self.assertEqual(product.rate, float_value)

    def test_autoincremental_values_return_as_none(self):
        product = factory(Product).make()
        self.assertIsNone(product.id)

    def test_autoincremental_values_return_specified_value(self):
        id_value = self.faker.random_int(min=42, max=288)
        product = factory(Product).make({
            'id': id_value
        })
        self.assertEqual(product.id, id_value)

    def test_max_string_length(self):
        product = factory(Product).make()

        self.assertLessEqual(len(product.short_name), FIELD_LENGTH)

    def test_ignored_columns(self):
        product = factory(Product).make(ignored_columns=['price'])
        self.assertIsNone(product.price)

    def test_specified_types(self):
        product = factory(Product).make(types={'description': 'email'})

        # Emails have only 1 '@'
        self.assertEqual(product.description.count('@'), 1)

        # Emails have at least one '.'
        self.assertTrue(product.description.count('.') >= 1)

    def test_mixed_custom_values_and_types(self):
        price_value = self.faker.random_int(min=42, max=288)

        product = factory(Product).make({'price': price_value}, types={'description': 'email'})  # nopep8

        self.assertEqual(product.price, price_value)

        # Emails have only 1 '@'
        self.assertEqual(product.description.count('@'), 1)

        # Emails have at least one '.'
        self.assertTrue(product.description.count('.') >= 1)

    def test_raises_value_error_if_faker_does_not_support_type(self):
        with self.assertRaises(ValueError):
            factory(Product).make(types={'description': 'foo'})

    def test_accepts_custom_faker_instance(self):
        faker = Faker.seed(0)
        product = factory(Product, faker).make()

        self.assertIsInstance(product, Product)

    def _prepare_database(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(bind=self.engine)

        with self.engine.begin() as connection:
            connection.execute(text(f'''
                CREATE TABLE products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255),
                    short_name VARCHAR({FIELD_LENGTH}),
                    description TEXT,
                    price INTEGER,
                    total_sells BIGINT,
                    is_active BOOLEAN,
                    created_at DATETIME,
                    promotion_day DATE,
                    promotion_hour DATETIME,
                    last_day_updates SMALLINT,
                    total_units NUMERIC,
                    rate FLOAT
                )
            '''))


if __name__ == '__main__':
    unittest.main()
