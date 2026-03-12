n = 42
result = []
temp = n
while temp:
    result.append(str(temp % 4))
    temp //= 4
print(f"42 (decimal) = {''.join(reversed(result))} (base-4) = {int(''.join(reversed(result)), 4)} check")
