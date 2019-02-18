# TODO - implement password cracking technique!
# opening development branch


def dictionary_attack():
    # start by defining an empty list of hashes
    hashes = []

    # load the formspring hash file and add each hash to the empty list defined above
    with open('/resources/formspring.txt') as formspring_file:
        for line in formspring_file:
            hashes.append(line.replace("\n", ""))

    # now define an empty set of passwords
    passwords = set()

    # load the password dictionary and add each password to the set
    # borrowed from crackstation.net
    with open('/resources/realhuman_phill.txt') as password_dictionary:
        for line in password_dictionary:
            passwords.add(line.replace("\n", ""))

    # now we have a list of hashes and a set of passwords - we can define our salt and get to cracking!
    # TODO - define salt

    return


if __name__ == '__main__':
    dictionary_attack()
