from typing import List


def compute_lps(pattern: str) -> List[int]:
    # Longest Proper Prefix that is suffix array
    lps = [0] * len(pattern)

    prefi = 0
    for i in range(1, len(pattern)):

        # Phase 3: roll the prefix pointer back until match or
        # beginning of pattern is reached
        while prefi and pattern[i] != pattern[prefi]:
            prefi = lps[prefi - 1]

        # Phase 2: if match, record the LSP for the current `i`
        # and move prefix pointer
        if pattern[prefi] == pattern[i]:
            prefi += 1
            lps[i] = prefi

        # Phase 1: is implicit here because of the for loop and
        # conditions considered above

    return lps


def kmp(pattern: str, text: str, pattern_lps=None) -> List[int]:
    match_indices = []
    if pattern_lps is None:
        pattern_lps = compute_lps(pattern)

    patterni = 0
    for i, ch in enumerate(text):

        # Phase 3: if a mismatch was found, roll back the pattern
        # index using the information in LPS
        while patterni and pattern[patterni] != ch:
            patterni = pattern_lps[patterni - 1]

        # Phase 2: if match
        if pattern[patterni] == ch:
            # If the end of a pattern is reached, record a result
            # and use infromation in LSP array to shift the index
            if patterni == len(pattern) - 1:
                match_indices.append(i - patterni)
                patterni = pattern_lps[patterni]

            else:
                # Move the pattern index forward
                patterni += 1

        # Phase 1: is implicit here because of the for loop and
        # conditions considered above

    return match_indices


def find_structures(string: (str, List), threshold=4):
    n = len(string)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if string[j] == string[i]:
                A[i][j] = A[i - 1][j - 1] + 1
    patterns = []
    indices_array = []
    for i in range(n):
        for j in range(n):
            length = A[i][j]
            if length >= threshold and ((i == n - 1 or j == n - 1) or A[i + 1][j + 1] <= length):
                pattern = string[j - length + 1:j + 1]
                print(pattern)
                if pattern not in patterns:
                    pattern_lps = compute_lps(pattern)
                    indices = kmp(pattern, string, pattern_lps)
                    patterns.append(pattern)
                    indices_array.append(indices)

    return patterns, indices_array


def edit_distance(freqs1: List[float], freqs2: List[float], mode: str = "direct"):
    if len(freqs1) != len(freqs2):
        raise ValueError("frequency list must be of same lenght")
    if len(freqs1) == 0:
        return 0
    if mode == "direct":
        return (1 / len(freqs1)) * sum(abs(freqs1[i] - freqs2[i]) for i in range(len(freqs1)))
    if mode == "interval":
        freqs1 = [freqs1[i + 1] - freqs1[i] for i in range(len(freqs1) - 1)]
        freqs2 = [freqs2[i + 1] - freqs2[i] for i in range(len(freqs2) - 1)]
        return edit_distance(freqs1, freqs2, mode="direct")
