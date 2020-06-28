import random
import datetime
from interruptingcow import timeout
TIMEOUT = 90

# def _stop(start_time, log=None, message=None):
#     if (datetime.datetime.now() - start_time).total_seconds() > TIMEOUT:
#         if log is not None:
#             log.info(message)
#         raise RuntimeError

class AlgorithmX:
    class Node:
        def __init__(self, tag=None):
            self.L = self
            self.U = self
            self.R = self
            self.D = self
            self.C = self
            self.S = 0
            self.tag = tag

    def __init__(self, cols, log=None):
        log.info("In __init__")
        assert cols >= 0, "Number of columns must be non-negative"
        self.cols = []
        self.rows = 0
        self.h = AlgorithmX.Node()

        last = self.h
        for col in range(cols):
            cur = AlgorithmX.Node()
            last.R = cur
            cur.L = last
            last = cur
            self.cols.append(cur)

        last.R = self.h
        self.h.L = last
        
    def appendRow(self, cols, tag=None, log=None):
        start_time = datetime.datetime.now()
        if tag is None:
            tag = self.rows

        cols = list(sorted(set(cols)))
        first = None
        last = None
        for idx in cols:
            #_stop(start_time, log=log, message='Timeout in appendRow')
            assert 0 <= idx < len(self.cols), "Column index must be between 0 and number of columns - 1"

            self.cols[idx].S += 1

            cur = AlgorithmX.Node(tag)
            if first is None:
                first = cur

            cur.U = self.cols[idx].U
            cur.U.D = cur
            cur.D = self.cols[idx]
            cur.D.U = cur
            cur.C = self.cols[idx]
            if last is not None:
                last.R = cur
                cur.L = last

            last = cur

        if first is not None:
            last.R = first
            first.L = last

        self.rows += 1

    def _cover(self, c, log=None):
        start_time = datetime.datetime.now()
        c.L.R = c.R
        c.R.L = c.L

        i = c.D
        while i != c:
            #_stop(start_time, log=log, message='Timeout in _cover (first while loop)')
            j = i.R
            start_time1 = datetime.datetime.now()
            while j != i:
                #_stop(start_time1, log=log, message='Timeout in _cover (second while loop)')
                j.U.D = j.D
                j.D.U = j.U
                j.C.S -= 1
                j = j.R
            i = i.D

    def _uncover(self, c, log=None):
        start_time = datetime.datetime.now()
        i = c.U
        while i != c:
            #_stop(start_time, log=log, message='Timeout in _uncover (first while loop)')
            j = i.L
            start_time1 = datetime.datetime.now()
            while j != i:
                #_stop(start_time1, log=log, message='Timeout in _uncover (second while loop)')
                j.U.D = j
                j.D.U = j
                j.C.S += 1
                j = j.L
            i = i.U
        c.L.R = c
        c.R.L = c

    def _solve(self, log):
        start_time = datetime.datetime.now()
        if self.h.R == self.h:
            yield []
            return

        if self.limit is not None:
            self.limit -= 1
            if self.limit < 0:
                return

        col = None
        cur = self.h.R
        while cur != self.h:
            #_stop(start_time, log=log, message='Timeout in _solve (first while loop)')
            if col is None or cur.S < col.S:
                col = cur
            cur = cur.R

        assert col is not None
        self._cover(col, log=log)

        start_time = datetime.datetime.now()
        r = col.D
        while r != col:
            #_stop(start_time, log=log, message='Timeout in _solve (second while loop)')
            cur = r.R
            start_time1 = datetime.datetime.now()
            while cur != r:
                #_stop(start_time1, log=log, message='Timeout in _solve (second while loop [first nested])')
                self._cover(cur.C, log=log)
                cur = cur.R

            start_time1 = datetime.datetime.now()
            for sol in self._solve(log=log):
                #_stop(start_time1, log=log, message='Timeout in _solve (second while loop [for loop])')
                yield [r.tag] + sol

            cur = r.L
            start_time1 = datetime.datetime.now()
            while cur != r:
                #_stop(start_time1, log=log, message='Timeout in _solve (second while loop [second nested])')
                self._uncover(cur.C, log=log)
                cur = cur.L

            r = r.D

        start_time = datetime.datetime.now()
        self._uncover(col, log=log)
        #_stop(start_time, log=log, message='Timeout in _solve (call to _uncover)')

    def solve(self, log, limit=None):
        self.limit = limit
        return self._solve(log=log)
