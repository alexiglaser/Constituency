import random
from interruptingcow import timeout
TIMEOUT = 180
import random

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
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                for col in range(cols):
                    cur = AlgorithmX.Node()
                    last.R = cur
                    cur.L = last
                    last = cur
                    self.cols.append(cur)

                last.R = self.h
                self.h.L = last
        except RuntimeError:
            log.info("Timeout in __init__")
            return None
        
    def appendRow(self, cols, tag=None, log=None):
#         log.info("In append 1")
        if tag is None:
            tag = self.rows

        #log.info("In append 2")
        cols = list(sorted(set(cols)))
        first = None
        last = None
        #log.info("In append 3")
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                for idx in cols:
#                     log.info(idx)
                    assert 0 <= idx < len(self.cols), "Column index must be between 0 and number of columns - 1"
                    #log.info("In append 4")

                    self.cols[idx].S += 1

                    #log.info("In append 5")
                    cur = AlgorithmX.Node(tag)
                    #log.info("In append 6")
                    if first is None:
                        first = cur
                    #log.info("In append 7")

                    cur.U = self.cols[idx].U
                    #log.info("In append 8")
                    cur.U.D = cur
                    #log.info("In append 9")
                    cur.D = self.cols[idx]
                    #log.info("In append 10")
                    cur.D.U = cur
                    #log.info("In append 11")
                    cur.C = self.cols[idx]
                    #log.info("In append 12")
#                     log.info(last)
                    if last is not None:
                        last.R = cur
                        cur.L = last
                    #log.info("In append 13")
                    
                    last = cur
                    #log.info("In append 14")
                    
                if first is not None:
                    last.R = first
                    first.L = last
                #log.info("In append 15")
                    
                self.rows += 1
                #log.info("In append 16")
        except RuntimeError:
            log.info("Could not append row due to timeout.")
            return None

    def _cover(self, c, log=None):
        c.L.R = c.R
        c.R.L = c.L

        i = c.D
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                while i != c:
                    j = i.R
                    while j != i:
                        j.U.D = j.D
                        j.D.U = j.U
                        j.C.S -= 1
                        j = j.R
                    i = i.D
        except RuntimeError:
            log.info("Timeout in _cover")
            return None

    def _uncover(self, c, log=None):
        i = c.U
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                while i != c:
                    j = i.L
                    while j != i:
                        j.U.D = j
                        j.D.U = j
                        j.C.S += 1
                        j = j.L
                    i = i.U
                c.L.R = c
                c.R.L = c
        except RuntimeError:
            log.info("Timeout in _uncover")
            return None

    def _solve(self, log):
#         log.info("Starting _solve")
        if self.h.R == self.h:
            yield []
            return

        if self.limit is not None:
            self.limit -= 1
            if self.limit < 0:
                return

        col = None
        cur = self.h.R
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                while cur != self.h:
                    if col is None or cur.S < col.S:
                        col = cur
                    cur = cur.R

                assert col is not None
                self._cover(col, log=log)
        except RuntimeError:
            log.info("Timeout in solve 1")
            return None

        r = col.D
        try:
            with timeout(TIMEOUT, exception=RuntimeError): 
                while r != col:
                    cur = r.R
                    try:
                        with timeout(TIMEOUT, exception=RuntimeError): 
                            while cur != r:
                                self._cover(cur.C, log=log)
                                cur = cur.R
                    except RuntimeError:
                        log.info("Timeout in solve 2")
                        return None

                    try:
                        with timeout(TIMEOUT, exception=RuntimeError): 
                            for sol in self._solve(log=log):
                                yield [r.tag] + sol
                    except RuntimeError:
                        log.info("Timeout in solve 3")
                        return None

                    cur = r.L
                    try:
                        with timeout(TIMEOUT, exception=RuntimeError): 
                            while cur != r:
                                self._uncover(cur.C, log=log)
                                cur = cur.L
                    except RuntimeError:
                        log.info("Timeout in solve 4")
                        return None

                    r = r.D

                try:
                    with timeout(TIMEOUT, exception=RuntimeError): 
                        self._uncover(col, log=log)
                except RuntimeError:
                    log.info("Timeout in solve 5")
                    return None
        except RuntimeError:
            log.info("Timeout in solve 6")
            return None

    def solve(self, log, limit=None):
        self.limit = limit
        return self._solve(log=log)
