import itertools

def generate_range(charset, length, start=None, end=None):
    all_combinations = [''.join(p) for p in itertools.product(charset, repeat=length)]
    
    if start and end:
        start_index = all_combinations.index(start)
        end_index = all_combinations.index(end)
        return all_combinations[start_index:end_index+1]
    
    return all_combinations