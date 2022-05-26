import math
import pyperclip


def encryptChar(char: str):
    return compress(ascii(char))


def ascii(num: str):
    return ord(num) - 31


def compress(num: int):
    if num >= 10:
        first = num % 10
        second = int(num / 10)
        result = first + second - 16
        if result < 0:
            hexy = hex(result)[3:]
            hexy = 'k' + hexy
            return [hexy, second]
        else:
            hexy = hex(result)[2:]
            return [hexy, second]
    else:
        return [str(num), 0]


def hexifier(string: str):
    hexgirl = ''
    if string[0] == 'k':
        hexgirl += '-0x' + string[1:]
    else:
        hexgirl += '0x' + string
    return int(hexgirl, 16)


def decrypt(values: list, keys: list):
    i = -1
    result = ''
    for x in values:
        i += 1
        value = hexifier(x)
        if x == '1' and keys[i] == 0:
            result += ' '
        else:
            if value <= 1:
                value += 16
            value -= keys[i]
            value = (keys[i] * 10) + value
            result += chr(value + 31)
    return result


class password:
    values = []
    keys = []
    name = ''

    def __init__(self, values: list, keys: list, name=''):
        self.values = values
        self.keys = keys
        self.name = name

    def setName(self, name: str):
        self.name = name


class record:
    values = []
    name: str

    def __init__(self, name: str, values: list):
        self.values = values
        self.name = name


def encrypt(string: str, name=''):
    values = []
    keys = []
    for x in string:
        result = encryptChar(x)
        values.append(result[0])
        keys.append(result[1])
    return password(values, keys, name)


def readPass():
    file = open('../data/manager_logs.txt')
    records = []
    name = ''
    for x in file:
        values = []
        lastk = False
        if x[0] != '#':
            for y in x:
                if y != '\n':
                    if lastk:
                        values.append('k' + y)
                        lastk = False
                    elif y == 'k':
                        lastk = True
                    else:
                        values.append(y)
                        lastk = False
            records.append(record(name, values))
            name = ''
        else:
            name = x[1:]
    file.close()
    return records


def readKeys():
    file = open('../data/kai_logs.txt')
    records = []
    name = ''
    for x in file:
        values = []
        if x[0] != '#':
            for y in x:
                if y != '\n':
                    values.append(int(y))
            records.append(record(name, values))
            name = ''
        else:
            name = x[1:]
    file.close()
    return records


def write(passwords: list[password]):
    filePass = open('../data/manager_logs.txt', 'w')
    fileKeys = open('../data/kai_logs.txt', 'w')
    for x in passwords:
        filePass.write('#' + x.name + '\n')
        fileKeys.write('#' + x.name + '\n')
        for y in x.values:
            filePass.write(y)
        for y in x.keys:
            fileKeys.write(str(y))
        filePass.write('\n')
        fileKeys.write('\n')
    filePass.close()
    fileKeys.close()


def main(passwords: list[password]):
    loop = True
    while loop:
        i = 0
        for x in passwords:
            i += 1
            print('[{}] {}'.format(i, x.name.replace('\n', '')))
        print('New')
        print('Quit')
        line = input('Select an option: ')
        if line.__contains__('quit'):
            return 'quit'
        elif line.isnumeric() and len(passwords) >= int(line) > 0:
            return 'show' + line
        elif line.__contains__('new'):
            return 'new'
        else:
            print('Invalid Input')


def show(password: password):
    pas = decrypt(password.values, password.keys)
    loop = True
    while loop:
        print(password.name.replace('\n', '') + ': ' + pas)
        pyperclip.copy(pas)
        line = input('[1] Edit\n[2] Back\n')
        if line == '1':
            return 'edit'
        elif line == '2':
            return 'main'
        else:
            print('Invalid input')


def edit(password: password):
    pas = decrypt(password.values, password.keys)
    loop = True
    while loop:
        print('Name: ' + password.name.replace('\n', ''))
        print('Password: ' + pas)
        line = input('[1] Edit Name\n[2] Edit Password\n')
        if line == '1':
            line = input('Enter new name: ')
            line2 = input('Re-enter new name: ')
            if line == 'back' or line2 == 'back':
                return 'back'
            elif line == line2:
                password.name = line
                return password
            else:
                print("Names don't match!")
        elif line == '2':
            line = input('Enter new password: ')
            line2 = input('Re-enter new password: ')
            if line == 'back' or line2 == 'back':
                return 'back'
            elif line == line2:
                newPassword = encrypt(line, password.name)
                return newPassword
            else:
                print("Passwords don't match!")
        elif line == 'back':
            return 'back'
        else:
            print('Invalid Input')

def new():
    loop = True
    name = ''
    pas = ''
    while loop:
        name = input('Enter Name: ')
        name2 = input('Re-enter Name: ')
        if name == 'back' or name2 == 'back':
            return 'back'
        elif name == name2:
            loop = False
        else:
            print("Names don't match!")
            name = ''
    loop = True
    while loop:
        pas = input('Enter Password: ')
        pas2 = input('Re-enter Password: ')
        if pas == 'back' or pas2 == 'back':
            return 'back'
        elif pas == pas2:
            loop = False
        else:
            print("Passwords don't match!")
            pas = ''
    return encrypt(pas, name)


values = readPass()
keys = readKeys()
passwords = []
for x in range(len(values)):
    value = values[x]
    key = keys[x]
    name = value.name
    passwords.append(password(value.values, key.values, name))

state = 'main'
on = True

while on:
    if state == 'main':
        state = main(passwords)
    elif state.__contains__('show'):
        tempState = show(passwords[int(state[4:]) - 1])
        if tempState.__contains__('edit'):
            state = 'edit' + state[4:]
        else:
            state = tempState
    elif state.__contains__('edit'):
        tempPass = edit(passwords[int(state[4:]) - 1])
        if tempPass == 'back':
            state = 'main'
        else:
            passwords[int(state[4:]) - 1] = tempPass
            write(passwords)
            state = 'show' + state[4:]
    elif state.__contains__('new'):
        pas = new()
        if pas == 'back':
            state = 'main'
        else:
            passwords.append(pas)
            write(passwords)
            state = 'main'
    elif state == 'quit':
        on = False
print('Shutting down...')
