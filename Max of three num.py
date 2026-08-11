#Program to print max of three numbers
def max_0f_two(x,y):
    if x>y:
        return x
    return y
def max_of_three(x,y,z):
    return max_0f_two(x,max_0f_two(y,z))
print(max_of_three(8,19,85))