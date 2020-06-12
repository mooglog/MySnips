"""Ideas and practice dealing with JSON API responses, then creating class objects out of them."""

from dictor import dictor
from datetime import datetime


class Base:
    """The base of the instance, we use the annotations to validate and select the fields we want from the JSON
    response.  This uses the module Dictor which flattens the JSON and allows us to pull the values we want from it"""
    attr1: str
    attr2: bool
    attr3: datetime
    attr4: int
    attr5: float

    def __init__(self, api_resp, *args, **kwargs):
        for field in self.__annotations__:
            mapped_field = kwargs['mapper'][field]
            if self.__annotations__[field] == datetime:
                value = dictor(api_resp, mapped_field)
                setattr(self, field, value)
                assert type(getattr(self, field, None)) == datetime
            elif self.__annotations__[field] == bool:
                value = dictor(api_resp, mapped_field)
                setattr(self, field, value)
            else:
                value = dictor(api_resp, mapped_field)
                setattr(self, field, value)

    def __repr__(self):
        return f"({self.attr1})"

    def __str__(self):
        for attr in self.__annotations__:
            print(f'{attr}: {str(getattr(self, attr))}')


class Item(Base):
    pass
