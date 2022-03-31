import unittest
from random import randint
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy_model_faker import factory


class Test(declarative_base()):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_text = Column(Text)
    test_integer = Column(Integer)


class test_factory(unittest.TestCase):
    engine = None  # type: engine.base.Engine
    session = None  # type: Session

    def test_factory_creates_model(self):
        self._prepare_database()

        amount = randint(1, 10)

        with self.session() as session:
            for _ in range(amount):
                test = factory(Test).make()  # type: Test
                session.add(test)
                session.commit()

        with self.session() as session:
            results = session.query(Test).all()
            self.assertEqual(len(results), amount)

    def test_model_persisted_with_specified_data(self):
        self._prepare_database()

        integer_value = randint(42, 288)
        text_value = 'lorem ipsum dolor sit amet'

        with self.session() as session:
            test = factory(Test).make({
                'test_integer': integer_value,
                'test_text': text_value
            })  # type: Test
            session.add(test)
            session.commit()

        with self.session() as session:
            test = session.query(Test).first()  # type: Test
            self.assertEqual(test.test_integer, integer_value)
            self.assertEqual(test.test_text, text_value)

    def test_autoincremental_values_return_as_none(self):
        test = factory(Test).make()
        self.assertIsNone(test.id)

    def test_autoincremental_values_return_specified_value(self):
        id_value = randint(42, 288)
        test = factory(Test).make({
            'id': id_value
        })
        self.assertEqual(test.id, id_value)

    def _prepare_database(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')
        self.session = sessionmaker(bind=self.engine)

        with self.engine.begin() as connection:
            connection.execute('''
                CREATE TABLE test (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_text TEXT,
                    test_integer INTEGER
                )
            ''')


if __name__ == '__main__':
    unittest.main()
