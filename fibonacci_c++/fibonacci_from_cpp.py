import datetime
import fibonacci_lib




if __name__ == "__main__":

    n = 10
    t1 = datetime.datetime.now()
    fib = fibonacci_lib.fibonacci(n)
    t2 = datetime.datetime.now()

    time_delta = (t2 - t1).total_seconds() * 1000

    print(f"Calculated the {n}tn number of the fibonaccisequence as {fib}")
    print(f"Operation took {time_delta} miliseconds")
