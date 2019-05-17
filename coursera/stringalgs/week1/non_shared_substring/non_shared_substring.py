# python3
import sys
import queue

kstart = 0
kend = 1
knode = 2
kparent = 1
kedge = 0

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
                        left_edge = text[lp]
                        new = n
                        tree[new] = tree[edge_end_node]
                        n += 1
                        tree[edge_end_node] = dict()
                        tree[edge_end_node][left_edge] = [lp, old_label_end, new]
                        
                        #right - the rest of the suffix
                        right_edge = text[tp]
                        new = n
                        tree[new] = dict()
                        n += 1
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

def build_parent_tree(tree):
    parent_tree = dict()
    for node in tree:
        for edge in tree[node]:
            child = tree[node][edge][knode]
            parent_tree[child] = [edge, node]
    
    return parent_tree

def print_tree(tree, text):
    for node in tree:
        for edge in tree[node]:
            print("{} -> {} : {}".format(
                node,
                tree[node][edge][knode],
                text[tree[node][edge][kstart]:tree[node][edge][kend]]
            ))

def mark_l_nodes(post_order, tree, parent_tree, hash_pos):
    l_nodes = dict()
    for node in post_order:
        if node == 0:
            continue;
        
        if not tree[node]:
            parent = parent_tree[node][kparent]
            edge = parent_tree[node][kedge]
            start = tree[parent][edge][kstart]
            end = tree[parent][edge][kend]
            if start <= hash_pos and end > hash_pos:
                l_nodes[node] = True
        else:
            all_children = True
            for edge in tree[node]:
                child = tree[node][edge][knode]
                if not child in l_nodes:
                    all_children = False
                    break
            if all_children:
                l_nodes[node] = True
    
    return l_nodes
    
        
              
def label_to_node(node, tree, parent_tree, text, hash_pos):
    path = []
    current = node
    while current > 0:
        parent = parent_tree[current][kparent]
        edge = parent_tree[current][kedge]
        if not tree[current]:
            if edge == '#':
                return None
            label = edge
        else:
            label = text[tree[parent][edge][kstart]:tree[parent][edge][kend]]
        path.append(label)
        current = parent
    
    label = "".join(reversed(path))
    
    return label
        
               
            
def solve(text1, text2):
    hash_pos = len(text1)
    text = text1 + '#' + text2 + '$'
    tree = build_suffix_tree(text)
    parent_tree = build_parent_tree(tree)
    
    #print('#', hash_pos)
    #print_tree(tree, text)
    #print(parent_tree)

    
    s = queue.LifoQueue()
    s.put(0)
    # leaves = []
    post_order = []
    while not s.empty():
        node = s.get()
        post_order.append(node)
        # if not tree[node]:
#             parent = parent_tree[node][kparent]
#             edge = parent_tree[node][kedge]
#             start = tree[parent][edge][kstart]
#             if start < hash_pos:
#                 leaves.append(node)
        for edge in tree[node]:
            s.put(tree[node][edge][knode])
            
    #print(post_order)
    
    l_nodes = mark_l_nodes(reversed(post_order), tree, parent_tree, hash_pos)
    
    #print(l_nodes)
    
    substring = ""
    min_len = -1
    for node in l_nodes:
        label = label_to_node(node, tree, parent_tree, text, hash_pos)
        if label == None:
            continue
        #print(node, label)
        label_len = len(label)
        if min_len < 0 or label_len < min_len:
            min_len = label_len
            substring = label
    
    
    return substring
            
if __name__ == '__main__':
    text1 = sys.stdin.readline ().strip ()
    text2 = sys.stdin.readline ().strip ()

    ans = solve(text1, text2)
    if ans:
        sys.stdout.write (ans + '\n')
