import random

def qs(lst):
    sort(lst, 0, len(lst) - 1)
    return 

def part(lst, left, right):
    pivot = random.randint(left, right)
    lst[left], lst[pivot] = lst[pivot], lst[left]
    i = left + 1
    pivot = lst[left]['radius']
    for j in range(left+1, right+1):
        if lst[j]['radius'] < pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i += 1
    pivot = i - 1
    lst[left], lst[pivot] = lst[pivot], lst[left]
    return pivot

def sort(lst, left, right):
    if left < right:
        ppos = part(lst, left, right)
        sort(lst, left, ppos-1)
        sort(lst, ppos+1, right)
    else:
        return 


