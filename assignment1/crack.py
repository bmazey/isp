# TODO - implement password cracking technique!
# opening development branch


def crack():
    # start by loading content from the resources folder
    with open('resources/formspring.txt') as f:
        form_data = f.read()

    # don't forget to close the files after reading
    f.close()

    # for testing
    print(form_data)

    return


if __name__ == '__main__':
    crack()
