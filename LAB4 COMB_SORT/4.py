#Comb Sort

def comb_sort(arr):
    n = len(arr)

    gap = n
    swapped = True

    while gap != 1 or swapped:
        gap = max(1, int(gap/1.3))
        swapped = False

        for i in range(0, n-gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True

    return arr

numbers = [8, 4, 1, 3, 2,7, 6, 5,]
print(numbers)
sorted_numbers = comb_sort(numbers.copy())
print(sorted_numbers)
