# SQLAlchemy Model Faker

<p align="center"><img height="150" alt="rogervila/sqlalchemy_model_faker" src="https://rogervila.es/static/img/sqlalchemy_model_faker.png" /></p>

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rogervila_sqlalchemy_model_faker&metric=coverage)](https://sonarcloud.io/dashboard?id=rogervila_sqlalchemy_model_faker)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rogervila_sqlalchemy_model_faker&metric=alert_status)](https://sonarcloud.io/dashboard?id=rogervila_sqlalchemy_model_faker)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=rogervila_sqlalchemy_model_faker&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=rogervila_sqlalchemy_model_faker)

Generate SQLAlchemy models with fake data.

> IMPORTANT: Documentation asumes previous knowledge on how to work with SQLAlchemy.

## Install

```sh
pip install sqlalchemy_model_faker
```

## Usage

The package expects a SQLAlchemy model that extends from `declarative_base()`.

It reads the model columns and generates a fake value according with the column type.

### Basic Usage

Let's create a Product model with a `description` and a `price` columns.

```python
from sqlalchemy.ext.declarative import declarative_base

class Product(declarative_base()):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    price = Column(Integer)
```

Use `factory` to create a fake `Product` model.

```python
from sqlalchemy_model_faker import factory

product = factory(Product).make()

print(type(product.description)) # <class 'str'>
print(type(product.price)) # <class 'int'>
```

Use [SQLAlchemy session](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#basics-of-using-a-session) to persist the `product` into the database.

### Custom values

By passing a dict, you can force `factory` to use custom provided values.

Other column values will be set with fake data.

```python
from sqlalchemy_model_faker import factory

product = factory(Product).make({'price': 288})

print(product.price) # 288
```

### Specific fake types

[Faker](https://faker.readthedocs.io/en/master/providers.html) has methods to generate fake data in a specific format, like emails, addresses, IPs, etc.

The fake data types can be specified passing a dict with column names and fake data types.

```python
from sqlalchemy_model_faker import factory

product = factory(Product).make(types={'description': 'email'})

# Emails have only 1 '@'
print(product.description.count('@')) # 1

# Emails have at least one '.'
print(product.description.count('.') # >= 1
```

Custom values and fake types can be passed together.

```python
from sqlalchemy_model_faker import factory

product = factory(Product).make({'price': 288}, types={'description': 'email'})

print(product.price) # 288
print(product.description) # valid email string
```

### Ignoring columns

Columns might be ignored. Their generated value will be `None`.

Other column values will be set with fake data.

```python
from sqlalchemy_model_faker import factory

product = factory(Product).make(ignored_columns=['price'])

print(product.price) # None
```

### Custom Faker instance

A custom faker instance can be passed to the `factory` constructor.

This is useful to extend Faker, or replace it with a Mock when running tests.

```python
from faker import Faker
from sqlalchemy_model_faker import factory

faker = Faker() # Extend Faker as needed or replace it with a Mock
product = factory(Product, faker).make()

# etc
```

## License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
