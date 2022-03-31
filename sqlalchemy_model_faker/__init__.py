#!/usr/bin/env python

from random import randint
from inspect import getmembers
from typing import Optional, Any
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

    # pylint: disable=dangerous-default-value
    def make(self, data: dict = {}, ignored: list = ['metadata', 'registry']):
        '''Generate SQLAlchemy Table instances with fake data'''

        for column in getmembers(self.entity):
            column_name = column[0]  # type: str

            if column_name.startswith('_') or column_name in ignored:
                continue

            column_data = column[1]  # type: InstrumentedAttribute

            if column_name not in data:
                data[column_name] = self._fake(column_data)

        return self.entity(**data)

    def _fake(self, column_data: InstrumentedAttribute) -> Any:
        '''Generate fake column data based on its type'''

        _type = str(column_data.type).lower()

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

        if _type == 'text':
            return self.faker.text()

        if _type == 'integer':
            return randint(0, 1000)

        # TODO: more column types support

        return None

    def _has_foreigns(self, column_data: InstrumentedAttribute) -> bool:
        foreign = str(column_data.foreign_keys)
        return foreign.startswith('{') and foreign.endswith('}')
