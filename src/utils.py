import random

def sorted(S):
    for i in range(len(S) - 1):
        if S[i] > S[i + 1]:
            return False
    return True


def randomindex(a, b):
    return random.randint(a, b)

def randomsort(n):
    iterations = 0

    S = [random.randint(1, 1000) for _ in range(n)]
    while not sorted(S):
        i = randomindex(0, len(S) - 2)
        j = randomindex(i + 1, len(S) - 1)

        if S[i] > S[j]:
            S[i], S[j] = S[j], S[i]
        iterations += 1
    if iterations == 0:
        return 1

    return iterations