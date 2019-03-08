

def pl_reverse(list):
    if not list:
        return []
    return [list.pop()] + pl_reverse(list)


if __name__ == '__main__':
    """ this function is for Programming Languages! """
    my_list = [1, 2, 3, 4]
    print("original: " + str(my_list))
    new_list = pl_reverse(my_list)
    print("reversed: " + str(new_list))
