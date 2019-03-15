
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("This is before the function is invoked!")
        func(*args, **kwargs)
        print("This is after the function is invoked!")
    return wrapper


def pl_reverse(my_list):
    if not my_list:
        return []
    return [my_list.pop()] + pl_reverse(my_list)


def factorial(n):
    if n < 2:
        return n * 1
    return n * factorial(n - 1)


@my_decorator
def greeting():
    print('hello!')


def my_closure(name):
    message = "Hi"

    def my_greeting():
        print(message + ' ' + name)

    my_greeting()


if __name__ == '__main__':
    """ this function is for Programming Languages! """
    my_list = [1, 2, 3, 4]
    print("original: " + str(my_list))
    new_list = pl_reverse(my_list)
    print("reversed: " + str(new_list))
    print(str(factorial(3)))
    greeting()
    my_closure("Kathy")
