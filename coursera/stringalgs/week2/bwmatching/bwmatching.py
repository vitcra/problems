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


def PreprocessBWT(bwt):
  """
  Preprocess the Burrows-Wheeler Transform bwt of some text
  and compute as a result:
    * starts - for each character C in bwt, starts[C] is the first position 
        of this character in the sorted array of 
        all characters of the text.
    * occ_count_before - for each character C in bwt and each position P in bwt,
        occ_count_before[C][P] is the number of occurrences of character C in bwt
        from position 0 to position P inclusive.
  """
  # Implement this function yourself
  pass


def CountOccurrences(pattern, bwt, starts, occ_counts_before):
  """
  Compute the number of occurrences of string pattern in the text
  given only Burrows-Wheeler Transform bwt of the text and additional
  information we get from the preprocessing stage - starts and occ_counts_before.
  """
  # Implement this function yourself
  return 0
     


if __name__ == '__main__':
  bwt = sys.stdin.readline().strip()
  # pattern_count = int(sys.stdin.readline().strip())
  # patterns = sys.stdin.readline().strip().split()

  # starts, occ_counts_before = PreprocessBWT(bwt)
  # occurrence_counts = []
  # for pattern in patterns:
  #   occurrence_counts.append(CountOccurrences(pattern, bwt, starts, occ_counts_before))
  # print(' '.join(map(str, occurrence_counts)))

  first_col = sorted(bwt)
  first_occurence = build_first_occurence_dict(first_col)
  count_occurence = build_count_occurence_dict(bwt, first_occurence)
  print(first_occurence)
  print(count_occurence)
