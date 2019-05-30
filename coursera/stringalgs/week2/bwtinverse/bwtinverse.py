# python3
import sys

def build_last_first_array(firstCol, lastCol):
  count = dict()
  first_col_index = dict()

  # index first col
  for i, char in enumerate(firstCol):
    if char in count:
      count[char] += 1
      c = count[char]
    else:
      c = 0
      count[char] = c
      first_col_index[char] = []

    first_col_index[char].append(i)

  last_first_array = []

  count = dict()

  for char in lastCol:
    if char in count:
      count[char] += 1
      c = count[char]
    else:
      c = 0
      count[char] = c
    
    last_first_array.append(first_col_index[char][c])
  
  return last_first_array

def InverseBWT(bwt):
    first_col = sorted(bwt)
    last_first_array = build_last_first_array(first_col, bwt)

    original = []

    current_index = 0
    while True:
        current_char = bwt[current_index]
        if current_char == '$':
            break
        original.append(current_char)
        current_index = last_first_array[current_index]
    
    return "".join(reversed(original)) + '$'


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT(bwt))