# python3
import sys

# NA = -1
#
# class Node:
#     def __init__ (self):
#         self.next = [NA] * 4

def build_trie(patterns):
    trie = dict()
    trie[0] = dict()
    
    for p in patterns:
        node = 0
        for edge in p:
            if edge in trie[node]:
                node = trie[node][edge]
            else:
                new = len(trie)
                trie[new] = dict()
                trie[node][edge] = new
                node = new 
    
    return trie

def solve(text, n, patterns):
    text_len = len(text)
    result = []
    trie = build_trie(patterns)
    for start_position in range(len(text)):
        current_position = start_position
        edge = text[current_position]
        node = 0
        while True:
            if not trie[node]:
                result.append(start_position)
                break
            elif edge in trie[node]:
                node = trie[node][edge]
                current_position +=1
                if current_position < text_len:
                    edge = text[current_position]
                else:
                    edge = None
            else:
                break
    
    return result

if __name__ == '__main__':
    text = sys.stdin.readline ().strip ()
    n = int (sys.stdin.readline ().strip ())
    patterns = []
    for i in range (n):
	    patterns += [sys.stdin.readline ().strip ()]

    ans = solve(text, n, patterns)

    sys.stdout.write (' '.join (map (str, ans)) + '\n')
