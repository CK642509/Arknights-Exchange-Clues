import itertools

def is_derangement(permutation):
    return all(i+1 != x for i, x in enumerate(permutation))

def generate_derangements(n):
    numbers = list(range(1, n+1))
    permutations = itertools.permutations(numbers)
    derangements = [p for p in permutations if is_derangement(p)]

    with open(f"derangements/derangement_{n}.txt", "w") as f:
        for derangement in derangements:
            f.write(" ".join(map(str, derangement)) + "\n")

if __name__ == '__main__':
    for i in range(3, 9):
        generate_derangements(i)
