# def log_function_call(func):
#     def wrapper(*args, **kwargs):
#         print(f"Calling function: {func.__name__}")
#         result = func(*args, **kwargs)
#         print(f"Function {func.__name__} returned: {result}")
#         return result
#     return wrapper

# @log_function_call
# def greet(name: str) -> str:
#     return f"Hello, {name}!"

# @log_function_call
# def add_numbers(a: int, b: int) -> int:
#     return a + b

# # Using the decorated functions
# greet("Alice")
# add_numbers(3, 5)
