import time


def timer(func):
    def wrapper():
        start = time.time()

        func()

        end = time.time()

        print(f"\nTime Taken: {end - start:.4f} seconds")

    return wrapper


@timer
def count_numbers():
    for i in range(1000000):
        pass


count_numbers()