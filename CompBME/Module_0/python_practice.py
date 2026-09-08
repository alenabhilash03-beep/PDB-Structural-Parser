# This is your first coding assignment for Computational BME.
# As discussed in class, feel free to use AI tools to help you complete this assignment, but remember to cite them.
# I encourage you to try the problems yourself first and only use AI tools when you are stuck to benefit your learning. 

# %% ###########################################################
# Problem 1: Practice writing pseudocode

# Write pseudocode that will input a integer N and output the sum of the first N numbers in the fibonacci sequence.
# Fibonacci sequence starts: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
# Example: If N = 5, the output should be 0 + 1 + 1 + 2 + 3 = 7

""" # you can use three double-quotes to write multi-line comments
N = input("Enter an integer")

a = 0
b = 1
total_sum = 0
for i from 1 to N:
    total_sum = total_sum + b
    next_val = a + b
    a = b
    b = next_val
Print total_sum
"""

# %% ###########################################################
# Problem 2: Comment your code
# Comments are very helpful for others (especially when pair-coding!) and yourself to understand your code! Add comments to the following code, which will run but produces the wrong output. Once you comment the code, you should be able to identify the error and fix it (the correct total that should be printed is 12).
N = 6 #Set N to 6, which is the number of fibonacci numbers to sum

a = 0 # set a to the first fibonacci number
b = 1 # set b to the second fibonacci number
count = 0 #Initializes counter
total = 0 #Initializes variable to keep track of sum

#While loop as long as counter is less than N
while count < (N - 1): #Fixed the code ("N - 1" instead of just "N")
    total = total + b #Adds the current number to the total

    next_value = a + b #Calculates the next fibonacci number
    a = b #Updates a to the current b (sort of like a sliding window)
    b = next_value #Updates b to the next fibonacci number, which is the sum of the two previous fibonacci numbers

    count = count + 1 #Updates value count

print(total) #Prints sum of N fibonacci numbers

# %% ###########################################################
# Problem 3: Using common Python libraries
# What is the standard deviation of the first 10 numbers in the fibonacci sequence? Use the numpy library to calculate the standard deviation.
import numpy as np
arr = np.array([0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
print(f"Standard deviation of the first 10 fibonacci numbers (rounded) is: {np.std(arr):.2f}")
# %% ###########################################################
# Problem 4: Don't repeat yourself by writing functions
# Write a function that takes an integer N as input and returns the sum of the first N numbers in the fibonacci sequence.
# Then use this function to calculate the sums for N = 5, 10, 15, 20, 25, and 30 and print them as a list.

#Defines function that takes integer N and returns the total sum of the first N values in the fibonacci sequence
def sum_fibonacci(N):
    a = 0
    b = 1
    total = 0
    count = 0
    while count < (N - 1):
        total += b
        next_value = a + b
        a = b
        b = next_value
        count += 1

    return total #Returns total value

values = [5, 10, 15, 20, 25, 30] 
fib_values = [sum_fibonacci(num) for num in values] #Finds fibonacci sum for each value in list values
print(fib_values)

# %% ###########################################################
# Problem 5: Read your error messages
# Run the following code block to see what the error messages are. Then, for each error:
# 1. Identify what type of error it is (SyntaxError, NameError, TypeError, etc.)
# 2. Add a comment to the line that is throwing the error explaining what the error is
# 3. Fix the error so that the code runs correctly

# You will only see one error at a time when you run the code. After fixing one error, run the code again to see the next error. Your final code should work correctly and will have comments where the original errors were.


def find_fib_above_limit(limit):
    """# The function inputs an integer called "limit" and finds the first number that goes above "limit" in the fibonacci sequence. It returns the index of that number.
    :param limit: limit of fibonacci sequence
    :type limit: integer
    :return: index of the first number above limit
    :rtype: integer
    """
    a = 0
    b = 1
    index = 0
    while int(a) <= limit: #TypeError, since a is a string, and it is being compared to an integer (in this case limit). Fixed by turning both a and b into integers.
        next_value = a + b
        a = b
        b = next_value
        index += 1# #Unbound local error, since index is getting 1 added to its value, but index currently does not even have a value (fixed by initializing index as 0)

    return index


result = find_fib_above_limit(8)
print("The index of the first number above your limit is: ", result)
# %% ###########################################################
# Problem 6: Test your code
# The following function will run but will output the wrong answer sometimes. Add test cases to verify that the function works correctly for a variety of inputs. If you find any inputs that produce incorrect outputs, fix the function. The function, when working properly, should return the sum of all odd Fibonacci numbers less than or equal to the input "limit".
def sum_odd_fib(limit):
    a, b = 0, 1 #Initializes a and b
    total = 0 #Sets total sum to 0

    #Loops as long as b is less than limit
    while b <= limit:
        if b % 2 == 1:  # This line checks if the Fibonacci number is odd
            total += b #Adds a to the total, since it is odd
        a, b = b, a + b #Updates a to b and b to the next value in the sequence
    return total #Returns total sum of all odd values before and equal to limit 

# Add your test cases here
assert sum_odd_fib(0) == 0
assert sum_odd_fib(1) == 2
assert sum_odd_fib(2) == 2
assert sum_odd_fib(4) == 5
assert sum_odd_fib(10) == 10
# %%
