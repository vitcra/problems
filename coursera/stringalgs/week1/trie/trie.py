#Uses python3
import sys

# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.
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


if __name__ == '__main__':
    patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))
