""" quicksort.py
from https://www.cuantum.tech/app/section/41-divide-and-conquer-algorithms-ecd63b96c8dc4f919456d4a54ea43fb7
"""
function quicksort(array):
   if length of array < 2:
      return array
   else:
      pivot = array[0]
      less = [i for i in array[1:] if i <= pivot]
      greater = [i for i in array[1:] if i > pivot]
      return quicksort(less) + [pivot] + quicksort(greater)

