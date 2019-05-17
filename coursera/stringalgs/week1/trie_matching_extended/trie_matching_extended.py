# python3
import sys
import random

# NA = -1
#
# class Node:
#     def __init__ (self):
#         self.next = [NA] * 4

def build_trie(patterns):
    trie = dict()
    trie[0] = dict()
    tl = len(trie)
    
    for p in patterns:
        newp = True
        node = 0
        for edge in p:
            if edge in trie[node]:
                node = trie[node][edge] 
            else:
                if newp and (node > 0) and (not trie[node]):
                     trie[tl] = dict()
                     trie[node]['*'] = tl  
                     tl += 1
                
                newp = False
                trie[tl] = dict()
                trie[node][edge] = tl
                node = tl
                tl += 1
        
        if trie[node] and ('*' not in trie[node]):
            trie[tl] = dict()
            trie[node]['*'] = tl
            tl += 1 
    
    return trie

def solve(text, n, patterns):
    text_len = len(text)
    result = []
    trie = build_trie(patterns)
    
    # for node in trie:
    #     for c in trie[node]:
    #         print("{}->{}:{}".format(node, trie[node][c], c))

    for start_position in range(len(text)):
        current_position = start_position
        edge = text[current_position]
        node = 0
        while True:
            if not trie[node] or '*' in trie[node]:
                result.append(start_position)
                break
            elif edge in trie[node]:
                node = trie[node][edge]
                current_position +=1
                edge = text[current_position] if current_position < text_len else None
            else:
                break
    
    return result

# N = 100
#
# def random_string(size):
#     chars = 'AAAAAAAAAAT';
#     return ''.join(random.choice(chars) for _ in range(size))
#
# def gen():
#     text = random_string(N)
#     patterns = []
#     for i in range(10):
#         patterns.append(random_string(8))
#
#     return (text, patterns)
#
# def solve_bf(text, n, patterns):
#     result = []
#     o_text = text
#     for i in range(len(text)):
#         for p in patterns:
#             if p == text[i:(i+len(p))]:
#                 result.append(i)
#     return list(set(result))


if __name__ == '__main__':
    text = sys.stdin.readline ().strip ()
    n = int (sys.stdin.readline ().strip ())
    patterns = []
    for i in range (n):
        patterns += [sys.stdin.readline ().strip ()]

    ans = solve(text, n, patterns)

    sys.stdout.write (' '.join (map (str, ans)) + '\n')

    # for i in range(50):
#         print(i)
#         text, patterns = gen()
#         result1 = solve(text, N, patterns)
#         result2 = solve_bf(text, N, patterns)
#         if result1 != result2:
#             print(result1)
#             print(result2)
#             print(text)
#             print(patterns)
#             break
