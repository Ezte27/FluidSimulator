list = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

print(f"List before: {list}")
list.remove((1, -1))
print(f"List after: {list}")