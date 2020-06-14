"""Random object model and decorator experiments"""

from functools import wraps
import random
import json


def announce(method):
    """Decorates methods, and prints the name of the method currently running."""
    @wraps(method)
    def wrapper(instance, *args, **kwargs) -> object:
        print(f'Running {method.__name__}, {method.__doc__}')
        resp = method(instance, *args, **kwargs)
        try:
            print(f'Response {resp["message"]}')
        except TypeError:
            print(resp)
    return wrapper


def limiter(method):
    """Will only allow decorated methods to run x number of times"""
    @wraps(method)
    def wrapper(instance, *args, **kwargs) -> object:
        _change_limit = 20
        instance.audit_tick()
        if instance.audit > _change_limit:
            print(f'Sorry you have modified the Thing t00 many times! Times: {instance.audit}')
        else:
            return method(instance, *args, **kwargs)
    return wrapper


class Thing:
    """This is a Thing, it stands high on it's pedestal, gleaming in the sunlight"""
    name: str
    size: int
    polarity: bool
    x: float
    y: float
    z: float

    audit = 0

    def __init__(self, *args, **kwargs):
        for field in self.__annotations__:
            try:
                setattr(self, field, kwargs[field])
            except KeyError:
                setattr(self, field, None)

    def __repr__(self):
        return f'Thing({self.name}, {self.size}, {self.polarity})'

    def __add__(self, other):
        pass  # TODO

    def polynomial(self):
        pass

    @classmethod
    def audit_tick(cls):
        cls.audit += 1

    @limiter
    @announce
    def bigger(self, amount, exponential=False) -> dict:
        """This makes a thing bigger, one always need one of these"""
        _old_size = self.size
        try:
            assert exponential is False
            self.size = amount
        except AssertionError:
            self.size = _old_size * amount
        message = f'The {self} has changed in size by {self.size - _old_size}'
        return dict(size=self.size, message=message)

    @limiter
    @announce
    def flip_polarity(self) -> dict:
        """
        This will reverse the current polarity, either true or false, whichever is opposite. In the words of David Byrne
        "Making Flippy Floppy"

        """
        _old = self.polarity
        self.polarity = not self.polarity
        message = f'The polarity was changed from {_old} to {self.polarity}'
        return dict(size=self.polarity, message=message)

    @announce
    def blocking_calls(self):
        """
        Lets say we have to make long costly blocking calls to an api or a database query that we can yield
        one by one
        """
        from time import sleep
        for i in range(10):
            sleep(2.875)
            yield random.random(1, 10000000000)

    def dict(self):
        return vars(self)

    def json(self):
        return json.dumps(vars(self))


class DerivedThing(Thing):
    """
    Lets modify the class by adding some additional attrs, and perhaps a method, using inheritance but also make
    sure that the original class supports the methods we expect it to.
    """
    state: dict

    def __init_subclass__(cls, **kwargs):

        return super().__init__()

    def __call__(self, *args, **kwargs):

        return f'Hey, a derived thing, It exists for no reason!'


def main():
    from random import randint as rando
    thing = Thing(name='The Thing', size=10, polarity=True)
    other_thing = DerivedThing()
    thing.bigger(rando(1, 100))
    thing.flip_polarity()
    thing.bigger(20, exponential=True)

    print(thing.dict())
    print(thing.json())

    some_things = [  # a simulated API type response
        {'name': f'Thing {rando(1,90)}',
         'size': 10,
         'polarity': True,
         'x': rando(1, 69),
         'y': rando(1, 69),
         'z': rando(1, 69)}
        for i in range(169)
    ]
    print(f'Now we instantiate all these random things we just made.')

    things = [Thing(**i) for i in some_things]

    print(f'There are {len(things)} Things')


if __name__ == '__main__':
    main()


