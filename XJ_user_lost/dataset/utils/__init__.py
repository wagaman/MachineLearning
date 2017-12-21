# Import the other utility functions
import inspect
from io import BlockingIOError
import locale
import math
import os
import pkg_resources
import platform
from random import uniform

if not platform.system() == 'Windows':
    import fcntl
else:
    import gevent.os

def nonblocking_readlines(f):
    """Generator which yields lines from F (a file object, used only for
       its fileno()) without blocking.  If there is no data, you get an
       endless stream of empty strings until there is data again (caller
       is expected to sleep for a while).
       Newlines are normalized to the Unix standard.
    """
    fd = f.fileno()
    if not platform.system() == 'Windows':
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    enc = locale.getpreferredencoding(False)

    buf = bytearray()
    while True:
        try:
            if not platform.system() == 'Windows':
                block = os.read(fd, 8192)
            else:
                block = gevent.os.tp_read(fd, 8192)
        except (BlockingIOError, OSError):
            yield ""
            continue

        if not block:
            if buf:
                yield buf.decode(enc)
            break

        buf.extend(block)

        while True:
            r = buf.find(b'\r')
            n = buf.find(b'\n')
            if r == -1 and n == -1:
                break

            if r == -1 or r > n:
                yield buf[:(n + 1)].decode(enc)
                buf = buf[(n + 1):]
            elif n == -1 or n > r:
                yield buf[:r].decode(enc) + '\n'
                if n == r + 1:
                    buf = buf[(r + 2):]
                else:
                    buf = buf[(r + 1):]

from . import constants, log, fun
#from . import (  # noqa
#        log,
#        fun,
#        constants,
#)
#from . import constants, image, time_filters, errors, forms, routing, auth  # noqa
