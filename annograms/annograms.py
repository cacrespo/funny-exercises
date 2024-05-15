# To avoid loading the word list on every call
WORDS = [w.rstrip() for w in open('WORD.lst')]


def annograms(word):
    """
    Returns a list of anagrams of the given word using words from WORD.lst.

    Args:
        word (str): The word for which to find anagrams.

    Returns:
        list: A list of valid anagrams of the input word.
    """

    results = [w for w in WORDS if sorted(word) == sorted(w) and word != w]
    return results


if __name__ == "__main__":
    print(annograms("train"))
    print('--')
    print(annograms('drive'))
    print('--')
    print(annograms('python'))
