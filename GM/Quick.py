import random

def qs(lst, dependencies):
    sort(lst, dependencies, 1, len(lst) - 1)
    return 

def part(lst, deps, left, right):
    pivot = random.randint(left, right)
    lst[left], lst[pivot] = lst[pivot], lst[left]
    deps[left], deps[pivot] = deps[pivot], deps[left]
    i = left + 1
    pivot = lst[left]['radius']

    for j in range(left+1, right+1):
        if lst[j]['radius'] + 2 < pivot:
            
            lst[i]['x'], lst[j]['x'] = lst[j]['x'], lst[i]['x']
            lst[i]['y'], lst[j]['y'] = lst[j]['y'], lst[i]['y']
            lst[i]['z'], lst[j]['z'] = lst[j]['z'], lst[i]['z']
            lst[i]['radius'], lst[j]['radius'] = lst[j]['radius'], lst[i]['radius']
            lst[i]['mass'], lst[j]['mass'] = lst[j]['mass'], lst[i]['mass']
            
            deps[i]['x'], deps[j]['x'] = deps[j]['x'], deps[i]['x']
            deps[i]['y'], deps[j]['y'] = deps[j]['y'], deps[i]['y']
            deps[i]['z'], deps[j]['z'] = deps[j]['z'], deps[i]['z']

            i += 1

    pivot = i - 1
    lst[left], lst[pivot] = lst[pivot], lst[left]

    lst[left]['x'], lst[pivot]['x'] = lst[pivot]['x'], lst[left]['x']
    lst[left]['y'], lst[pivot]['y'] = lst[pivot]['y'], lst[left]['y']
    lst[left]['z'], lst[pivot]['z'] = lst[pivot]['z'], lst[left]['z']
    lst[left]['radius'], lst[pivot]['radius'] = lst[pivot]['radius'], lst[left]['radius']
    lst[left]['mass'], lst[pivot]['mass'] = lst[pivot]['mass'], lst[left]['mass']
    return pivot

def sort(lst, deps, left, right):
    if left < right:
        ppos = part(lst, deps, left, right)
        sort(lst, deps, left, ppos-1)
        sort(lst, deps, ppos+1, right)
    else:
        return 


