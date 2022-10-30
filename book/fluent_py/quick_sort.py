import numpy as np

def partition(l, left, right):
    key = left
    slow = left
    # [3, 5, 28, 36, 51, 34, 29, 99, 91, 64]
    for fast in range(left+1, right+1):
        if l[fast]<l[key]:
            l[fast], l[slow]=l[slow], l[fast]
            if fast!=right:
                slow+=1
    l[slow], l[key]=l[key], l[slow]
    return slow


def quick_sort(input_list, left, right):
    if left<right:
        mid = partition(input_list, left, right)
        print(mid)
        quick_sort(input_list, left, mid-1)
        quick_sort(input_list, mid+1, right)



if __name__=="__main__":
    # test = list(set(np.random.randint(0, 100, 10)))
    test = [3, 5, 28, 36, 51, 34, 29, 99, 91, 64]
    quick_sort(test, 0, len(test)-1)
    # partition(test, 0, len(test)-1)
    print(test)
