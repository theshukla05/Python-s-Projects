my_list = [10, 20, 30, 40, 50]

# Prevent division by zero error for empty lists
if len(my_list) > 0:
    list_mean = sum(my_list) / len(my_list)
else:
    list_mean = 0

print(f"The mean is: {list_mean}")