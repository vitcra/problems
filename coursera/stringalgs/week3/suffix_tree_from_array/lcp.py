# python3

def build_inverted_sa(sa):
    L = len(sa)
    inverted = [0] * L

    for i, j in enumerate(sa):
        inverted[j] = i

    return inverted

def get_lcp_suffixes(text, offsetA, offsetB, init):
    L = len(text)
    lcp = max(0, init)
    while offsetA+lcp < L and offsetB+lcp < L:
        if text[offsetA+lcp] == text[offsetB+lcp]:
            lcp += 1
        else:
            break
    
    return lcp

def build_lcp_array(text, sa):
    L = len(text)
    lcp_array = [0] * (L-1)
    inverted_sa = build_inverted_sa(sa)

    suffix = sa[0]
    lcp = 0
    for _ in range(L):
        pos_sa = inverted_sa[suffix]
        if pos_sa == L-1:
            lcp = 0
            suffix = (suffix+1) % L
            continue
        next_suffix = sa[pos_sa+1]
        lcp = get_lcp_suffixes(text, suffix, next_suffix, lcp-1)
        lcp_array[pos_sa] = lcp
        suffix = (suffix + 1) % L
    
    return lcp_array

if __name__ == '__main__':
    text = "ATATATA$"
    sa = [7, 6, 4, 2, 0, 5, 3, 1]
    print(build_lcp_array(text, sa))