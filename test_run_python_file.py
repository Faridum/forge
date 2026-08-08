from functions.run_python_file import run_python_file


print("Test 1:")
print(run_python_file("calculator", "main.py"))

print("\nTest 2:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("\nTest 3:")
print(run_python_file("calculator", "tests.py"))

print("\nTest 4:")
print(run_python_file("calculator", "../main.py"))

print("\nTest 5:")
print(run_python_file("calculator", "nonexistent.py"))

print("\nTest 6:")
print(run_python_file("calculator", "lorem.txt"))