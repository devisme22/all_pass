from random import randint, shuffle


def password_crafter(a):
    #variable setup
    password = [0]
    string = ''

    #Set of characters
    character = 'abcdefghijklmnopqrstuvxyz_-+!@#$%^&*())[:>?"{|;1234567890'

    #Password body
    for items in range(0, a):
        r = randint(0, 56)
        password.append(character[r])

    #first letter of the password
    first_letter = randint(0, 24)
    password[0] = (character[first_letter].capitalize())

    #random capitalizer
    #capitaler = randint(1, 16)
    #password[capitaler].capitalize()

    return(string.join(password))


if __name__ == '__main__':
    password_crafter(17)
