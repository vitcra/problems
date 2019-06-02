# python3
import sys

def build_char_order(text):
    L = len(text)
    alphabet = {'$': 0, 'A': 1, 'C': 2, 'G': 3, 'T': 4}
    A = len(alphabet)
    count = [0] * A
    order = [0] * L
    
    for i in range(L):
        char = text[i]
        count[alphabet[char]] += 1
    
    # convert counts to tails
    for i in range(1, A):
        count[i] += count[i-1]
    
    for i in reversed(range(0, L)):
        char = text[i]
        j = alphabet[char]
        count[j] -= 1
        order[count[j]] = i
        
    
    return order
        
def build_char_classes(text, order):
    L = len(text)
    classes = [0] * L
    A = 0
    
    for i in range(1, L):
        if text[order[i]] != text[order[i-1]]:
            A += 1
        
        classes[order[i]] = A
    
    return classes, A + 1
        

def build_doubled_order(text, N, order, classes, A):
    L = len(text)
    new_order = [0] * L
    count = [0] * A
    
    for i in range(L):
        count[classes[i]] += 1
    
    for i in range(1, A):
        count[i] += count[i-1]
    
    for i in reversed(range(L)):
        j = (order[i] - N + L) % L
        cl = classes[j]
        count[cl] -= 1
        new_order[count[cl]] = j
    
    return new_order

def build_doubled_classes(doubledOrder, N, classes):
    A = 0
    L = len(doubledOrder)
    new_classes = [0] * L
    
    for i in range(1, L):
        cur = doubledOrder[i]
        prev = doubledOrder[i-1]
        mid = (cur + N) % L
        mid_prev = (prev + N) % L
        if classes[cur] != classes[prev] or classes[mid] != classes[mid_prev]:
            A += 1
        new_classes[cur] = A
    
    return new_classes, A+1
    
    
   
def build_suffix_array(text):
    L = len(text)
    order = build_char_order(text)
    classes, A = build_char_classes(text, order)
    N = 1
    while N < L: 
        order = build_doubled_order(text, N, order, classes, A)
        classes, A = build_doubled_classes(order, N, classes)
        N *= 2
    
    return order


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))