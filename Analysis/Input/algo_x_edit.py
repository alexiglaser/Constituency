from collections import defaultdict
from collections.abc import Iterator
from random import shuffle, choice

class ExactCover(Iterator):
    """An iterator that yields solutions to an EXACT COVER problem.

    An EXACT COVER problem consists of a set of "choices". Each choice
    satisfies one or more "constraints". Choices and constraints may
    be represented by any hashable Python objects, with the proviso
    that all choices must be distinct, as must all constraints.

    A solution is a list of choices such that each constraint is
    satisfied by exactly one of the choices in the solution.

    """
    """
    2020/04/16  Whilst using this code has been great there are two issues
    which mean that it doesn't really work for the problem being calculated
    at the moment.
    1. It gives all know solutions, however on some occasions this takes too 
        long so we would only really require say 1,000 or 10,000.
    2. Since we are only wanting a sub-sample of results would like to have 
        some more randomness into
        the results.
    """
    
    # This implements Donald Knuth's "Algorithm X"
    # http://lanl.arxiv.org/pdf/cs/0011047.pdf

    def __init__(self, constraints, initial=(), random=False, n=None):
        """Construct an ExactCover solver,

        Required argument:
        constraints -- A map from each choice to an iterable of
            constraints satisfied by that choice.

        Optional arguments:
        initial -- An iterable of choices that must appear in every
            solution. (Default: no choices.)
        random -- Generate solutions in random order? (Default: False.)

        For example:

            >>> next(ExactCover(dict(A = [1, 4, 7],
            ...                      B = [1, 4],
            ...                      C = [4, 5, 7],
            ...                      D = [3, 5, 6],
            ...                      E = [2, 3, 6, 7],
            ...                      F = [2, 7])))
            ['B', 'D', 'F']

        """
        """
        2020/04/16 Added 'n' as an argument - only return 'n' solutions 
            (if 'n' is less than total number of solutions then all solutions 
            are returned).
        """
        self.random = random
        self.constraints = constraints

        # A map from constraint to the set of choices that satisfy
        # that constraint.
        self.choices = defaultdict(set)
        for i in self.constraints:
            for j in self.constraints[i]:
                self.choices[j].add(i)

        # The set of constraints which are currently unsatisfied.
        self.unsatisfied = set(self.choices)

        # The partial solution currently under consideration,
        # implemented as a stack of choices.
        self.solution = []

        # Make all the initial choices.
        try:
            for i in initial:
                self._choose(i)
            self.iter = self._solve()
        except KeyError:
            # Initial choices were contradictory, so there are no solutions.
            self.iter = iter(())

    def __next__(self):
        return next(self.iter)

    def _solve(self):
        if not self.unsatisfied:
            # No remaining unsatisfied constraints.
            yield list(self.solution)
            return

#         # Pick the constraint with the fewest remaining choices
#         # (Knuth's "S heuristic").
#         best = min(self.unsatisfied, key=lambda j:len(self.choices[j]))
#         choices = list(self.choices[best])
        # Pick a starting point at random
        pick = choice(list(unsatisfied))
        choices = list(self.choices[pick])
        if self.random:
            shuffle(choices)

        # Try each choice in turn and recurse.
        for i in choices:
            self._choose(i)
            yield from self._solve()
            self._unchoose(i)
#             if n is not None:
#                 if len(list(self.solution)) == n:
#                     yield list(self.solution)
#                     return

    def _choose(self, i):
        """Make choice i; mark constraints satisfied; and remove any
        choices that clash with it.

        """
        self.solution.append(i)
        for j in self.constraints[i]:
            self.unsatisfied.remove(j)
            for k in self.choices[j]:
                for l in self.constraints[k]:
                    if l != j:
                        self.choices[l].remove(k)

    def _unchoose(self, i):
        """Unmake choice i; restore constraints and choices."""
        last = self.solution.pop()
        assert i == last
        for j in self.constraints[i]:
            self.unsatisfied.add(j)
            for k in self.choices[j]:
                for l in self.constraints[k]:
                    if l != j:
                        self.choices[l].add(k)
