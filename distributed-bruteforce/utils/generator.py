import itertools

def generate_all(charset, length):
    return [''.join(p) for p in itertools.product(charset, repeat=length)]

def split_list(data, n):
    k = len(data) // n
    return [data[i*k:(i+1)*k] for i in range(n-1)] + [data[(n-1)*k:]]