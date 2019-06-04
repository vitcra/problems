# python3
import sys

kedges = 0
kparent = 1
knedge = 2
kdepth = 3
kchild = 0
kstart = 1
kend = 2

def suffix_array_to_suffix_tree(sa, lcp, text):
    """
    Build suffix tree of the string text given its suffix array suffix_array
    and LCP array lcp_array. Return the tree as a mapping from a node ID
    to the list of all outgoing edges of the corresponding node. The edges in the
    list must be sorted in the ascending order by the first character of the edge label.
    Root must have node ID = 0, and all other node IDs must be different
    nonnegative integers. Each edge must be represented by a tuple (node, start, end), where
        * node is the node ID of the ending node of the edge
        * start is the starting position (0-based) of the substring of text corresponding to the edge label
        * end is the first position (0-based) after the end of the substring corresponding to the edge label

    For example, if text = "ACACAA$", an edge with label "$" from root to a node with ID 1
    must be represented by a tuple (1, 6, 7). This edge must be present in the list tree[0]
    (corresponding to the root node), and it should be the first edge in the list (because
    it has the smallest first character of all edges outgoing from the root).
    """

    L = len(text)
    tree = {0:[[], None, None, 0]}
    N = 0
    lcpPrev = 0
    curNode = 0
    prevNode = 0

    for i, start in enumerate(sa):
      while tree[curNode][kdepth] > lcpPrev:
        prevNode = curNode
        curNode = tree[curNode][kparent]
      
      offset = lcpPrev - tree[curNode][kdepth]
      if offset == 0:
        # Create new node
        new_start = start + lcpPrev
        e = len(tree[curNode][kedges])
        N += 1
        tree[N] = [[], curNode, e, L - new_start]
        tree[curNode][kedges].append([N, new_start, L])
        curNode = N
      else:
        # Split
        edge = tree[prevNode][knedge]
        edge_start = tree[curNode][kedges][edge][kstart]
        edge_end = tree[curNode][kedges][edge][kend]

        # left
        left_start = edge_start + offset
        tree[prevNode][kdepth] = lcpPrev
        tree[curNode][kedges][edge][kend] = left_start
        
        e = len(tree[prevNode][kedges])
        N += 1
        tree[N] = [[], prevNode, e, tree[prevNode][kdepth] + L - left_start]
        tree[prevNode][kedges].append([N, left_start, L])

        # right
        right_start = start + lcpPrev
        e += 1
        N += 1
        tree[N] = [[], prevNode, e, tree[prevNode][kdepth] + L - right_start]
        tree[prevNode][kedges].append([N, right_start, L])
        curNode = N
      
      if i < L - 1:
        lcpPrev = lcp[i]

    return tree


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    sa = list(map(int, sys.stdin.readline().strip().split()))
    lcp = list(map(int, sys.stdin.readline().strip().split()))
    print(text)
    # Build the suffix tree and get a mapping from 
    # suffix tree node ID to the list of outgoing Edges.
    tree = suffix_array_to_suffix_tree(sa, lcp, text)
    """
    Output the edges of the suffix tree in the required order.
    Note that we use here the contract that the root of the tree
    will have node ID = 0 and that each vector of outgoing edges
    will be sorted by the first character of the corresponding edge label.
    
    The following code avoids recursion to avoid stack overflow issues.
    It uses two stacks to convert recursive function to a while loop.
    This code is an equivalent of 
    
        OutputEdges(tree, 0);
    
    for the following _recursive_ function OutputEdges:
    
    def OutputEdges(tree, node_id):
        edges = tree[node_id]
        for edge in edges:
            print("%d %d" % (edge[1], edge[2]))
            OutputEdges(tree, edge[0]);
    
    """
    #print(tree)
    stack = [(0, 0)]
    result_edges = []
    while len(stack) > 0:
      (node, edge_index) = stack[-1]
      stack.pop()
      if not node in tree or not tree[node][kedges]:
        continue
      edges = tree[node][kedges]
      if edge_index + 1 < len(edges):
        stack.append((node, edge_index + 1))
      print("%d %d" % (edges[edge_index][kstart], edges[edge_index][kend]))
      stack.append((edges[edge_index][kchild], 0))
