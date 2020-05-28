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

    def __init__(self, cols):
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

    def appendRow(self, cols, tag=None):

        if tag is None:
            tag = self.rows

        cols = list(sorted(set(cols)))
        first = None
        last = None
        for idx in cols:
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

    def _cover(self, c):
        c.L.R = c.R
        c.R.L = c.L

        i = c.D
        while i != c:
            j = i.R
            while j != i:
                j.U.D = j.D
                j.D.U = j.U
                j.C.S -= 1
                j = j.R
            i = i.D

    def _uncover(self, c):
        i = c.U
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

    def _solve(self):
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
            if col is None or cur.S < col.S:
                col = cur
            cur = cur.R

        assert col is not None
        self._cover(col)

        r = col.D
        while r != col:
            cur = r.R
            while cur != r:
                self._cover(cur.C)
                cur = cur.R

            for sol in self._solve():
                yield [r.tag] + sol

            cur = r.L
            while cur != r:
                self._uncover(cur.C)
                cur = cur.L

            r = r.D

        self._uncover(col)

    def solve(self, limit=None):
        self.limit = limit
        return self._solve()
