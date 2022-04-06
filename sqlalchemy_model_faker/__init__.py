#!/usr/bin/env python

import re
from inspect import getmembers
from typing import Optional, Any
from uuid import uuid4
from sqlalchemy.orm.attributes import InstrumentedAttribute
from faker import Faker


class factory:
    '''Generate entity objects with fake data'''

    entity = None
    faker = None  # type: Faker

    # TODO: define 'entity' type by resolving declarative_base()
    def __init__(self, entity, faker: Optional[Faker] = None) -> None:
        self.entity = entity
        self.faker = Faker() if faker is None else faker

    def make(self, data: Optional[dict] = None, types: Optional[dict] = None, ignored_columns: list = []):
        '''Generate SQLAlchemy Table instances with fake data'''
        data = {} if data is None else data
        types = {} if types is None else types

        for column in getmembers(self.entity):
            column_name = column[0]  # type: str

            if column_name.startswith('__') or column_name in ignored_columns:
                continue

            column_data = column[1]  # type: InstrumentedAttribute

            if column_name not in data:
                data[column_name] = self._fake(column_data, types)

        return self.entity(**data)

    def _fake(self, column_data: InstrumentedAttribute, types: dict) -> Any:
        '''Generate fake column data based on its type'''

        if not hasattr(column_data, 'type'):
            return None

        # Autoincrement values should not be faked.
        #
        # autoincrement property could return 'auto' string which is evaluated
        # as True, so we ensure that comparison is made with a boolean value.
        #
        # pylint: disable=singleton-comparison
        if column_data.autoincrement == True:
            return None

        # TODO: investigate handling foreign_keys instead of returning None
        if self._has_foreigns(column_data):
            return None

        # Example: self.faker.email()
        if column_data.key in types.keys():
            try:
                method = getattr(self.faker, types[column_data.key])
                return method()
            except Exception as e:
                raise ValueError(f'Faker does not support "{types[column_data.key]}" method') from e  # nopep8

        _type = str(column_data.type).lower().strip()

        if _type in ('biginteger', 'bigint'):
            return self.faker.random_int(min=0, max=10000)

        if _type in ('boolean', 'bool'):
            return self.faker.boolean()

        if _type == 'date':
            return self.faker.date_time().date()

        if _type == 'datetime':
            return self.faker.date_time()

        if _type in ('float', 'numeric'):
            return float(self.faker.random_int(min=100, max=1000)) / 10

        if _type in ('integer', 'int'):
            return self.faker.random_int(min=0, max=1000)

        if _type in ('smallinteger', 'smallint'):
            return self.faker.random_int(min=0, max=1)

        # pylint: disable=anomalous-backslash-in-string
        string_length = re.search('varchar\((\d+)\)', _type)
        if string_length is not None:
            return self.faker.sentence()[:int(string_length.group(1))]

        if _type in ('string', 'str', 'varchar'):
            return self.faker.sentence()

        if _type == 'text':
            return self.faker.text()

        if _type == 'time':
            return self.faker.date_time().time()

        if _type in ('uuid', 'uniqueidentifier'):
            return uuid4()

        return None

    def _has_foreigns(self, column_data: InstrumentedAttribute) -> bool:
        foreign = str(column_data.foreign_keys)
        return foreign.startswith('{') and foreign.endswith('}')
