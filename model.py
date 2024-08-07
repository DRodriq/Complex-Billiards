
PRIMES = []

def genesis():
    global PRIMES
    if len(PRIMES) == 0:
        PRIMES.append(3)
        return 3
    else:
        last = PRIMES[-1]
        for i in range(last + 1, last*2):
            for j in range(2, i):
                if i % j == 0:
                    break
            else:
                PRIMES.append(i)
                return i

def hash_prime(prime):
    for i in range(len(PRIMES)):
        if PRIMES[i] == prime:
            return i
    return -1