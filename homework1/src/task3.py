def check_number(num):
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    return "zero"

def first_10_primes():
    primes = []
    num = 2
    while len(primes) < 10:
        if all(num % i != 0 for i in range(2, num)):
            primes.append(num)
        num += 1
    return primes

def sum_1_to_100():
    total = 0
    i = 1
    while i <= 100:
        total += i
        i += 1
    return total