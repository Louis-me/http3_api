__author__ = "shikun"
from gevent import Greenlet
from gevent import monkey; monkey.patch_all()
class requestGevent(Greenlet):
    def __init__(self, func):
        Greenlet.__init__(self)
        self.func = func
    def _run(self):
        # gevent.sleep(self.n)
        self.func