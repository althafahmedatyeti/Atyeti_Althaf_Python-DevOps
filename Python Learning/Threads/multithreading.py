import concurrent.futures
numbers = list(range(1, 101))
def partial_sum(nums):
    return sum(nums)
chunk_size = 25
chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
total_sum = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(partial_sum, chunks)
    for partial in results:
        total_sum += partial
print("Total sum:", total_sum)








