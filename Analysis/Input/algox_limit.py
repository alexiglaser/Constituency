"""
As it was proving too difficult to change the code for the ExactCover class to
limit the output, it was decide to try and see if a function could be written to
replicate what was needed (e.g. limit the results to 'n')
"""

from collections import defaultdict
from collections.abc import Iterator
from random import shuffle, choice


def ExactCoverConst(constraints, random=False, n=None):
    # A map from constraint to the set of choices that satisfy
    # that constraint.
    print(1)
    choices = defaultdict(set)
    for i in constraints:
        for j in constraints[i]:
            choices[j].add(i)
    print(2)
    # The set of constraints which are currently unsatisfied.
    unsatisfied = set(choices)
    print(3)
    # The partial solution currently under consideration,
    # implemented as a stack of choices.
    solution = []
    print(4)
    # Make all the initial choices.
    try:
        iter = solve()
    print(5)
    
def __next__(iter):
    return next(iter)

def _solve(unsatisfied, solution, choices, random):
    if not unsatisfied:
        # No remaining unsatisfied constraints.
        yield list(solution)
        return

#         # Pick the constraint with the fewest remaining choices
#         # (Knuth's "S heuristic").
#         best = min(self.unsatisfied, key=lambda j:len(self.choices[j]))
#         choices = list(self.choices[best])
    # Pick a starting point at random
    pick = choice(list(unsatisfied))
    picked = list(choices[pick])
    if random:
        shuffle(picked)

    # Try each choice in turn and recurse.
    for i in choices:
        _choose(i)
        yield from _solve()
        _unchoose(i)
#             if n is not None:
#                 if len(list(self.solution)) == n:
#                     yield list(self.solution)
#                     return

    def _choose(solution, constraints, unsatisfied, choices, i):
        """Make choice i; mark constraints satisfied; and remove any
        choices that clash with it.

        """
        solution.append(i)
        for j in constraints[i]:
            unsatisfied.remove(j)
            for k in choices[j]:
                for l in constraints[k]:
                    if l != j:
                        choices[l].remove(k)

    def _unchoose(solution, constraints, unsatisfied, choices, i):
        """Unmake choice i; restore constraints and choices."""
        last = solution.pop()
        assert i == last
        for j in constraints[i]:
            unsatisfied.add(j)
            for k in choices[j]:
                for l in constraints[k]:
                    if l != j:
                        choices[l].add(k)
