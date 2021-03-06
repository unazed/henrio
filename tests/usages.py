"""
Ignore this file, this is some test usages
"""

from henrio import *
import sys
from unittest import TestCase


class Tests(TestCase):
    async def sleeper(self, tim):
        a = await sleep(tim)
        print(a)
        return "Bon hommie"

    async def sleeperator(self):
        return await self.sleeper(4)

    async def duo(self):
        await self.sleeperator()

    async def raser(self):
        raise IndexError("Oh no")

    def test_run_files(self):
        loop = IOCPLoop() if sys.platform == "win32" else SelectorLoop()
        with open("testfile.hio", 'rb') as file:
            print(file.fileno())
            print(sys.platform, loop, getattr(loop, "wrap_file", "N'existe pas!"))
            wrapped = loop.wrap_file(file)

            async def do_thing():
                print(await wrapped.read(1024))

            loop.run_until_complete(do_thing())

    def test_run_socks(self):
        try:
            import socket
            loop = IOCPLoop() if sys.platform == "win32" else SelectorLoop()
            r, w = socket.socketpair()

            # w.send(b"Elle me dit ecris un chanson")
            async def do_thing():
                reader, writer = await wrap_socket(r), await wrap_socket(w)
                await writer.send(b"abcdefg")
                print(b'asd')
                await writer.send(b"dsa")
                print(b'dsa')
                f = await reader.recv(12)
                print(f, 1)
                await writer.send(b"1234")
                d = await reader.recv(1024)
                print(d, 2)

            loop.run_until_complete(do_thing())
        finally:
            r.close()
            w.close()

    def test_run_socks2(self):
        try:
            raise Exception
            import socket
            loop = IOCPLoop() if sys.platform == "win32" else SelectorLoop()
            rw = socket.socket()
            rw.connect(("irc.mindfang.org", 6667))

            # w.send(b"Elle me dit ecris un chanson")
            async def do_thing():
                sock = await wrap_socket(rw)
                await sock.send(b"NICK henry\r\n")
                print(b'dsa')
                f = await sock.recv(32)
                print(f, 1)
                await sock.send(b"1234238012480192481024\n")
                print(12321)
                d = await sock.recv(15)
                print(d, 2)

            loop.run_until_complete(do_thing())
        finally:
            rw.close()

    def test_run_stdio(self):
        import sys
        loop = SelectorLoop()
        reader, writer = loop.wrap_file(sys.stdin), loop.wrap_file(sys.stdout)
        loop.create_task(writer.write("asd"))
        resp = loop.run_until_complete(reader.read(10))
        print(resp)

    def test_run_thing(self):
        l = BaseLoop()
        d = Future()

        async def s():
            await sleep(10)
            d.set_result(32)

        async def g():
            return await d

        l.create_task(s())
        print(l.run_until_complete(g()))

    def test_bier(self):
        def asd():
            yield from sleep(4)
            yield
            print("dun")

        l = BaseLoop()
        l.run_until_complete(asd())

    def test_working(self):
        async def asd():
            def b():
                import time
                a = time.monotonic()
                time.sleep(4)
                print(time.monotonic() - a)
                return 3

            d = await threadworker(b)
            print(d)

        l = BaseLoop()
        l.run_until_complete(asd())

    def async_working(self):
        raise Exception
        l = SelectorLoop()
        import socket

        async def do_thing():
            r, w = socket.socketpair()
            reader, writer = l.wrap_socket(r), l.wrap_socket(w)
            print('asd')
            await writer.send(b"asdasd!")
            print("dsa")
            f = r.recv(5)
            print(f)
            return 3

        f = l.run_until_complete(async_threadworker(do_thing))
        print(f)

    def test_get_looper(self):
        import types
        l = SelectorLoop()

        @types.coroutine
        def gl():
            l = yield ("loop",)
            return l

        print(l.run_until_complete(gl()))

    def test_test_spawn(self):
        async def mf():
            print("asd")
            await spawn(f2())

        async def f2():
            await sleep(3)
            print(1)

        run(mf())

    def test_ctask(self):
        async def pepe():
            return await current_task()

        l = SelectorLoop()
        f = l.run_until_complete(pepe())
        print(f, type(f))

    def test_locktests(self):
        d = 0
        lock = Lock()

        async def pepe():
            nonlocal d
            async with lock:
                print(2)
                await sleep(4)
                print(5)
                d = 2

        async def pepo():
            nonlocal d
            async with lock:
                print(3)
                await sleep(7)
                print(4)
                d = 3

            print(lock._queue)

        l = SelectorLoop()
        l.create_task(pepo())
        l.run_until_complete(pepe())

    def test_timeouts(self):
        async def myfunc():
            import time
            try:
                print(time.time())
                async with timeout(3):
                    print("cake")
                    loop = await get_loop()
                    print(loop._timers, 'afd', loop.time())
                    await sleep(10)
                    print("nyet")
            except Exception as e:
                print(type(e), "asd")
                print(time.time())
            else:
                print(time.time())
                print("shit!")

        l = BaseLoop()
        l.run_until_complete(myfunc())

    def test_dawait(self):
        class AClass:
            @staticmethod
            def __iter__():
                for x in range(3):
                    print("pass")
                    yield ("sleep", 2)

            __await__ = __iter__

        run(AClass)

    #def test_workers(self):
    #    run(processworker(print, 123, 456, 32))
