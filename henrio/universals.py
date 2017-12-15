"""
These are all the functions and classes that will work perfectly fine outside of henrio. Each of these *should*
work with other libraries like asyncio or curio or trio (or really any other async library that uses a standard
method of operation)
"""

from . import Future, Task, Conditional
from . import Queue, HeapQueue
from . import sleepinf

import typing
from math import inf
from time import monotonic
import select
from types import coroutine

__all__ = ["Future", "Task", "Conditional", "Queue", "HeapQueue", "sleepinf", "sleep", "timeout", "AsyncFile"]


@coroutine
def sleep(seconds: typing.Union[float, int]):
    """Sleep for a specified amount of time. Will work with any library."""
    if seconds == 0:
        yield
    elif seconds == inf:
        yield from sleepinf()
    else:
        end = monotonic() + seconds
        while end >= monotonic():
            yield


class timeout:
    def __init__(self, coro, timeout):
        if hasattr(coro, "__await__"):
            self._coro = coro.__await__()
        else:
            self._coro = coro
        self._finish = monotonic() + timeout

    def __iter__(self):
        try:
            val = None
            while monotonic() < self._finish:
                val = yield self._coro.send(val)
            else:
                raise TimeoutError
        except StopIteration as err:
            return err.value

    __await__ = __iter__

    def send(self, data):
        if monotonic() < self._finish:
            return self._coro.send(data)
        raise TimeoutError

    def throw(self, data):
        if monotonic() < self._finish:
            return self._coro.throw(data)
        raise TimeoutError


class AsyncFile:
    def __init__(self, file):
        self.file = file

    @coroutine
    def recv(self, nbytes):
        cond = Conditional(lambda: select.select([self.file], [], [], 0)[0])
        yield from cond
        return self.file.recv(nbytes)

    @coroutine
    def read(self, nbytes):
        cond = Conditional(lambda: select.select([self.file], [], [], 0)[0])
        yield from cond
        return self.file.read(nbytes)

    @coroutine
    def send(self, data):
        cond = Conditional(lambda: select.select([], [self.file], [], 0)[1])
        yield from cond
        return self.file.send(data)

    @coroutine
    def write(self, data):
        cond = Conditional(lambda: select.select([], [self.file], [], 0)[1])
        yield from cond
        return self.file.write(data)

    @coroutine
    def accept(self):
        cond = Conditional(lambda: select.select([self.file], [], [], 0)[0])
        yield from cond
        return self.file.accept()

    def fileno(self):
        return self.file.fileno()

    def close(self):
        self.file.close()