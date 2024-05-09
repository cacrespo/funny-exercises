import itertools


WORDS = {w.rstrip() for w in open('WORD.lst')}  # a set to improve performance


def annograms(word):
    """
    Returns a set of anagrams of the given word using words from WORD.LST.

    Args:
        word (str): The word for which to find anagrams.

    Returns:
        set: A set of valid anagrams of the input word.
    """
    permutations = itertools.permutations(word)

    results = {''.join(permut)
               for permut in permutations if ''.join(permut) in WORDS}
    return results  # results is a set too to avoid duplicates ;-)


if __name__ == "__main__":
    print(annograms("train"))
    print('--')
    print(annograms('drive'))
    print('--')
    print(annograms('python'))
