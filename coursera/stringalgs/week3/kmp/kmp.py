# python3
import sys

def build_prefix_array(text):
    prefix_array = [0]
    border = 0
    for i in range(1, len(text)):
        while (border > 0) and (text[i] != text[border]):
            border = prefix_array[border-1]
        
        if text[i] == text[border]:
            border += 1
        else:
            border = 0
        
        prefix_array.append(border)
    
    return prefix_array

def find_pattern(pattern, text):
    """
    Find all the occurrences of the pattern in the text
    and return a list of all positions in the text
    where the pattern starts in the text.
    """
    
    prefix_array = build_prefix_array(pattern + '$' + text)
    #print(prefix_array)
    
    T = len(text)
    P = len(pattern)
    result = []
    for i in range(P+1, T+P+1):
        if prefix_array[i] == P:
            result.append(i - 2 * P)
    
    return result


if __name__ == '__main__':
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    result = find_pattern(pattern, text)
    print(" ".join(map(str, result)))

