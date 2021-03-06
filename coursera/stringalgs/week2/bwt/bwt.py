# python3
import sys
import functools

def build_suffix_array(text):
    L = len(text)
    def cmp_func(offsetA, offsetB):
        m = min(L-offsetA, L-offsetB)
        for i in range(m):
            cmp_char = (text[offsetA+i] > text[offsetB+i]) - (text[offsetA+i] < text[offsetB+i])
            if cmp_char != 0:
                return cmp_char
            i += 1
        
        return 0
    
    return sorted(range(L), key=functools.cmp_to_key(cmp_func))

def burrows_wheeler_transform(text):
    suffix_array = build_suffix_array(text)
    bwt = []
    for index in suffix_array:
        end = index-1 if index > 0 else suffix_array[0]
        bwt.append(text[end])
    return "".join(bwt)

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(burrows_wheeler_transform(text))