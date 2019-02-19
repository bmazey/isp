import hashlib
import platform


def dictionary_attack():

    # test - apparently I was using a 32-bit python distro >_>;
    print(platform.architecture())

    # start by defining an empty list of hashes
    hashes = []

    # load the formspring hash file and add each hash to the empty list defined above
    with open('resources/formspring.txt', 'r') as formspring_file:
        for line in formspring_file:
            hashes.append(line.replace("\n", ""))

    # now define an empty set of passwords
    passwords = set()

    # load the password dictionary and add each password to the set
    # borrowed from crackstation.net
    with open('resources/realhuman_phill.txt', 'r', encoding='UTF-8', errors='ignore') as password_dictionary:
        for line in password_dictionary:
            passwords.add(line.replace("\n", ""))

    # now we have a list of hashes and a set of passwords - we can define our salt and get to cracking!
    salt = list(range(10, 100))

    # let the cracking begin!
    # this will be our cracked password counter
    cracked = 0

    # iterate over the password set applying the salt, hashing, then comparing to the formspring hash list
    for password in passwords:
        for num in salt:
            # notice that here the salt is a number from 10 - 100 concatenated with the password
            salted = (str(num) + password)
            digest = hashlib.sha256(salted.encode('utf-8')).hexdigest()
            if digest in hashes:
                cracked += 1
                print('password detected! salt: ' + str(num) + ' password: ' + password)

    # print the total
    print('total passwords cracked: ' + str(cracked))

    return


if __name__ == '__main__':
    """ this is our main driver method for the formspring dictionary attack """
    dictionary_attack()
