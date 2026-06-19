def log_call(func):
    def wrapper(*args, **kwargs):
        print("\nFunction Name:", func.__name__)
        print("Arguments:", args)

        result = func(*args, **kwargs)

        print("Returned:", result)

        return result

    return wrapper


@log_call
def add(a, b):
    return a + b


@log_call
def greet(name):
    return f"Hello {name}"


@log_call
def square(n):
    return n * n


print(add(10, 20))
print(greet("Hiba"))
print(square(6))