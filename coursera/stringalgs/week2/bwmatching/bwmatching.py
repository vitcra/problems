# python3
import sys

def build_first_occurence_dict(firstCol):
  first_occurence = dict()

  for i, char in enumerate(firstCol):
    if char in first_occurence:
      continue
    else:
      first_occurence[char] = i
  
  return first_occurence

def build_count_occurence_dict(lastCol, firstOccurenceDict):
  count_occurence = dict()
  characters = firstOccurenceDict.keys()

  for char in characters:
    count_occurence[char] = [0]

  # index first col
  for char in lastCol:
    for dc in count_occurence:
      j = count_occurence[dc][-1]
      if dc == char:
        j += 1
      count_occurence[dc].append(j)
  
  return count_occurence


def count_pattern_occurence(pattern, bwt, firstOccurence, countOccurence):
  top = 0
  bottom = len(bwt) - 1
  
  while top <= bottom:
      if pattern == "":
          return bottom - top + 1
      else:
          char = pattern[-1]
          if char not in firstOccurence:
              return 0

          pattern = pattern[:-1]
          count_top = countOccurence[char][top]
          count_bottom = countOccurence[char][bottom+1]
          if count_bottom > count_top:
              top = firstOccurence[char] + count_top
              bottom = firstOccurence[char] + count_bottom - 1
          else:
              return 0
     


if __name__ == '__main__':
  bwt = sys.stdin.readline().strip()
  pattern_count = int(sys.stdin.readline().strip())
  patterns = sys.stdin.readline().strip().split()
  
  first_col = sorted(bwt)
  first_occurence = build_first_occurence_dict(first_col)
  count_occurence = build_count_occurence_dict(bwt, first_occurence)
  # print(first_occurence)
#   print(count_occurence)

  occurrence_counts = []
  for pattern in patterns:
    occurrence_counts.append(count_pattern_occurence(pattern, bwt, first_occurence, count_occurence))
  print(' '.join(map(str, occurrence_counts)))
