"""Random decorator experiments"""

from functools import wraps
import random


def announce(method):
    @wraps(method)
    def wrapper(instance, *args, **kwargs) -> object:
        print(f'Running {method.__name__}, {method.__doc__}')
        resp = method(instance, *args, **kwargs)
        try:
            print(f'Response {resp["message"]}')
        except TypeError:
            print(resp)
    return wrapper


def security(method):
    @wraps(method)
    def wrapper(instance, *args, **kwargs) -> object:
        instance.audit_tick()
        if instance.audit > 10:
            print(f'Sorry you have modified the Thing toooo many times! Times: {instance.audit}')
        else:
            return method(instance, *args, **kwargs)
    return wrapper


class Thing:
    """This is a Thing, it stands high on it's pedestal, gleaming in the sunlight"""
    name: str
    size: int
    polarity: bool

    audit = 0

    def __init__(self, *args, **kwargs):
        for field in self.__annotations__:
            try:
                setattr(self, field, kwargs[field])
            except KeyError:
                setattr(self, field, None)

    def __repr__(self):
        return f'Thing({self.name}, {self.size}, {self.polarity})'

    @classmethod
    def audit_tick(cls):
        cls.audit += 1

    @security
    @announce
    def bigger(self, *args) -> dict:
        """This makes a thing bigger!"""
        _old_size = self.size
        self.size = args[0]
        message = f'The {self} has changed in size by {self.size - _old_size}'
        return dict(size=self.size, message=message)

    @security
    @announce
    def flip_polarity(self) -> dict:
        """This will reverse the current polarity, either true or false, whichever is opposite."""
        _old = self.polarity
        self.polarity = not self.polarity
        message = f'The polarity was changed from {_old} to {self.polarity}'
        return dict(size=self.polarity, message=message)


    @announce
    def blocking_calls(self):
        """Lets say we have to make long costly blocking calls to an api, that we can yield one by one"""
        from time import sleep
        for i in range(10):
            sleep(2.875)
            yield random.random(1, 10000000000)



class DerivedThing(Thing):
    """
    Lets modify the class by adding some additional attrs, and perhaps a method, using inheritance but also make
    sure that the original class supports the methods we expect it to.
    """
    state: dict

    def __init_subclass__(cls, **kwargs):

        return super().__init__()


def main():
    from random import randint as rando
    thing = Thing(name='test', size=10, polarity=True)
    other_thing = DerivedThing()
    for i in range(12):
        thing.bigger(rando(1, 100))
        thing.flip_polarity()
        thing.blocking_calls()


if __name__ == '__main__':
    main()


