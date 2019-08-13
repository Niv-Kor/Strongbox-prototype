def zeroPadding(num, pad):
    result = str(num)
    digits = countDigits(num)

    for _ in range(pad - digits):
        result = '0' + result

    return result


def countDigits(num):
    counter = 0
    while num > 0:
        counter += 1
        num /= 10

    return counter


# Get all prime numbers within a range, using the segmented sieve algorithm
def primeList(lo, hi):
    # Mark all numbers as prime
    primes = [True] * (hi - lo)

    # Eliminate 0 and 1, if necessary
    for i in range(lo, min(2, hi)):
        primes[i - lo] = False

    ihi = int(hi ** 0.5)
    for i in _potentialPrimes():
        if i > ihi:
            break

        # find first multiple of i: i >= i*i and i >= lo
        ilo = max(i, 1 + (lo - 1) // i) * i

        # determine how many multiples of i >= ilo are in range
        n = 1 + (hi - ilo - 1) // i

        # mark them as composite
        primes[ilo - lo::i] = n * [False]

    return [i for i, v in enumerate(primes, lo) if v]


def _potentialPrimes():
    s = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)

    for i in s:
        yield i

    s = (1,) + s[3:]
    j = 30
    while True:
        for i in s:
            yield j + i
        j += 30


def isPrime(num):
    if num <= 1:
        return False

    # Iterate from 2 to n / 2
    for i in range(2, num // 2):
        # if num is divisible by any number between
        # 2 and n / 2, it is not prime
        if (num % i) == 0:
            return False

    return True
