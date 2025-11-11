test_cases = [
    1234,
    5678,
    910,
    4321
]
for num in test_cases:
    result = []
    num_str = str(num)
    for i in range(len(num_str)):
        digit = num_str[i]
        if digit == '0':
            continue
        zeros = len(num_str) - i - 1
        result.append(digit + '0' * zeros)
    print(", ".join(result))