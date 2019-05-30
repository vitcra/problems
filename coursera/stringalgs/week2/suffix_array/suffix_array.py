# python3
import sys

STYPE = ord('S')
LTYPE = ord('L')

def show_suffix_array(arr, pos=None):
  print(" ".join("%02d" % each for each in arr))
  if pos is not None:
    print(" ".join("^^" if each == pos else "  " for each in range(len(arr))))

def build_type_array(text):
  L = len(text)
  type_array = bytearray(L+1)
  type_array[-1] = STYPE
  
  if L == 0:
    return type_array
  
  type_array[-2] = LTYPE
  
  for i in reversed(range(L-1)):
    if text[i] < text[i+1]:
      type_array[i] = STYPE
    elif text[i] == text[i+1]:
      type_array[i] = type_array[i+1]
    else:
      type_array[i] = LTYPE

  return type_array

def is_lms_char(offset, typemap):
  if offset == 0:
    return False
  
  if typemap[offset] == STYPE and typemap[offset-1] == LTYPE:
    return True

  return False

def find_bucket_sizes(text, alphabetSize=256):
  sizes = [0] * alphabetSize

  for char in text:
    sizes[char] += 1
  
  return sizes

def find_bucket_heads(bucketSizes):
  offset = 1
  heads = []
  for size in bucketSizes:
    heads.append(offset)
    offset += size
  
  return heads

def find_bucket_tails(bucketSizes):
  offset = 1
  tails = []
  for size in bucketSizes:
    offset += size
    tails.append(offset-1)

  return tails

def guess_lms_sort(text, bucketSizes, typemap):
  L = len(text)
  guessedSuffixArray = [-1] * (L + 1)
  bucketTails = find_bucket_tails(bucketSizes)

  for i in range(L):
    if not is_lms_char(i, typemap):
      continue
    
    char = text[i]
    guessedSuffixArray[bucketTails[char]] = i
    bucketTails[char] -= 1

  guessedSuffixArray[0] = L
  return guessedSuffixArray

def induce_sort_l(text, suffixArray, bucketSizes, typemap):
  bucketHeads = find_bucket_heads(bucketSizes)

  for i in range(len(suffixArray)):
    if suffixArray[i] == -1:
      continue
    
    j = suffixArray[i] - 1
    if j < 0 or typemap[j] != LTYPE:
      continue
    
    char = text[j]
    suffixArray[bucketHeads[char]] = j
    bucketHeads[char] += 1
    #show_suffix_array(suffixArray, i)

def induce_sort_s(text, suffixArray, bucketSizes, typemap):
  bucketTails = find_bucket_tails(bucketSizes)

  for i in reversed(range(len(suffixArray))):
    if suffixArray[i] == -1:
      continue
    
    j = suffixArray[i] - 1
    if j < 0 or typemap[j] != STYPE:
      continue
    
    char = text[j]
    suffixArray[bucketTails[char]] = j
    bucketTails[char] -= 1
    #show_suffix_array(suffixArray, i)

def lms_substrings_are_equal(offsetA, offsetB, text, typemap):
  L = len(text)
  if offsetA == L or offsetB == L:
    return False
  
  i = 0
  while True:
    aIsLms = is_lms_char(offsetA + i, typemap)
    bIsLms = is_lms_char(offsetB + i, typemap)

    if (i>0 and aIsLms and bIsLms):
      return True
    
    if (aIsLms != bIsLms):
      return False
    
    if (text[offsetA + i] != text[offsetB + i]):
      return False
    
    i += 1

  return True

def summarise_suffix_array(text, suffixArray, typemap):
  L = len(text)
  lmsNames = [-1] * (L+1)
  currentName = 0

  lastLmsSuffixOffset = suffixArray[0]
  lmsNames[lastLmsSuffixOffset] = currentName

  for i in range(1, len(suffixArray)):
    suffixOffset = suffixArray[i]
    
    if suffixOffset == -1:
      continue
    
    if not is_lms_char(suffixOffset, typemap):
      continue
    
    if not lms_substrings_are_equal(lastLmsSuffixOffset, suffixOffset, text, typemap):
      currentName += 1
    
    lastLmsSuffixOffset = suffixOffset
    lmsNames[lastLmsSuffixOffset] = currentName

  summarySuffixOffsets = []
  summaryText = []
  for i, name in enumerate(lmsNames):
    if name == -1:
      continue
    
    summarySuffixOffsets.append(i)
    summaryText.append(name)

  summaryAlphabetSize = currentName + 1

  return summaryText, summaryAlphabetSize, summarySuffixOffsets

def accurate_lms_sort(text, bucketSizes, typemap, summarySuffixArray, summarySuffixOffsets):
  L = len(text)
  suffixOffsets = [-1] * (L + 1)

  bucketTails = find_bucket_tails(bucketSizes)
  for i in reversed(range(2, len(summarySuffixArray))):
    textIndex = summarySuffixOffsets[summarySuffixArray[i]]
    char = text[textIndex]
    suffixOffsets[bucketTails[char]] = textIndex
    bucketTails[char] -= 1
  
  suffixOffsets[0] = L
  return suffixOffsets

def make_summary_suffix_array(summaryText, summaryAlphabetSize):
  L = len(summaryText)
  if summaryAlphabetSize == L:
    summarySuffixArray = [-1] * (L + 1)
    summarySuffixArray[0] = L

    for i in range(L):
      j = summaryText[i]
      summarySuffixArray[j+1] = i

  else:
    summarySuffixArray = make_suffix_array_by_induced_sorting(summaryText, summaryAlphabetSize)
  
  return summarySuffixArray

def make_suffix_array_by_induced_sorting(text, alphabetSize):
  typemap = build_type_array(text)
  bucketSizes = find_bucket_sizes(text, alphabetSize)
  guessedSuffixArray = guess_lms_sort(text, bucketSizes, typemap)
  induce_sort_l(text, guessedSuffixArray, bucketSizes, typemap)
  induce_sort_s(text, guessedSuffixArray, bucketSizes, typemap)

  summaryText, summaryAlphabetSize, summarySuffixOffsets = \
         summarise_suffix_array(text, guessedSuffixArray, typemap)
  
  summarySuffixArray = make_summary_suffix_array(summaryText, summaryAlphabetSize)

  suffixArray = accurate_lms_sort(text, bucketSizes, typemap, summarySuffixArray, summarySuffixOffsets)
  induce_sort_l(text, suffixArray, bucketSizes, typemap)
  induce_sort_s(text, suffixArray, bucketSizes, typemap)

  return suffixArray

    

def build_suffix_array(text):
  """
  Build suffix array of the string text and
  return a list result of the same length as the text
  such that the value result[i] is the index (0-based)
  in text where the i-th lexicographically smallest
  suffix of text starts.
  """
  result = make_suffix_array_by_induced_sorting(text, 256)
  # Implement this function yourself
  return result


if __name__ == '__main__':
  s = sys.stdin.readline().strip()
  text = bytearray()
  text.extend(map(ord, s[:-1]))
  #text = b'cabbage'
  print(" ".join(map(str, build_suffix_array(text))))
