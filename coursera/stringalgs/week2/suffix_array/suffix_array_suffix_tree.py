# python3
import sys
import queue

kstart = 0
kend = 1
knode = 2

def build_suffix_tree(text):
    """
    Build a suffix tree of the string text and return a list
    with all of the labels of its edges (the corresponding 
    substrings of the text) in any order.
    """
    
    text_len = len(text)
    tree = dict()
    tree[0] = dict()
    n = len(tree)
    
    for suffix_start in range(text_len):
        #print("Suffix:", suffix_start)
        node = 0
        tp = suffix_start
        finished = False
        while not finished:
            #print("node", node)
            edge = text[tp]
            if edge in tree[node]:
                tp += 1
                edge_end_node = tree[node][edge][knode]
                
                # traverse edge label as long as it matches suffix
                for lp in range(tree[node][edge][kstart] + 1, tree[node][edge][kend]):
                    if text[lp] != text[tp]:
                        #print(lp, tp)
                        # split
                        old_label_end = tree[node][edge][kend]
                        tree[node][edge][kend] = lp
                        # left - the rest of the label
                        new = n
                        tree[new] = tree[edge_end_node]
                        n += 1
                        tree[edge_end_node] = dict()
                        left_edge = text[lp]
                        tree[edge_end_node][left_edge] = [lp, old_label_end, new]
                        
                        #right - the rest of the suffix
                        new = n
                        tree[new] = dict()
                        n += 1
                        right_edge = text[tp]
                        tree[edge_end_node][right_edge] = [tp, text_len, new]
                
                        #print("Split")
                        #print_tree(tree)
                        finished = True
                        break
                    tp += 1
                node = edge_end_node                 
            else:
                # brand new branch
                new = n
                tree[new] = dict()
                n += 1            
                tree[node][edge] = [tp, text_len, new]
                finished = True
                
                #print("New branch")
                #print_tree(tree)
    
    return tree

def print_tree(tree):
    for node in sorted(tree.keys()):
        for edge in sorted(tree[node].keys()):
            print("{} -> {} : {}, {}, {}".format(
                node,
                tree[node][edge][knode],
                edge,
                tree[node][edge][kstart],
                tree[node][edge][kend]
            ))

def get_suffix_tree_leaves(tree, node, offset):
    leaves = []
    for edge in sorted(tree[node].keys()):
        child = tree[node][edge][knode]
        child_start = tree[node][edge][kstart]
        more_offset = tree[node][edge][kend] - tree[node][edge][kstart]
        if not tree[child]:
            leaves.append(child_start - offset)
        else:
            leaves += get_suffix_tree_leaves(tree, child, offset + more_offset)
    
    return leaves



def build_suffix_array(text):
    tree = build_suffix_tree(text)
    return get_suffix_tree_leaves(tree, 0, 0)

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))