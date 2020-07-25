import random
import sqlite3


# conexion db
conn = sqlite3.connect('card.s3db')


# funciones con tablas
def show_balance(id_account):
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT balance FROM card WHERE id = {id_account} ;')
    except:
        balance = 0
    finally:
        balance = 0

    for c in cur.fetchall():
        balance = c[0]
    conn.commit()
    print(f'\nBalance: {balance}')


def add_income(id_account):
    print('\nEnter income:')
    income = int(input())

    cur = conn.cursor()
    try:
        cur.execute(f'UPDATE card SET balance = balance + {income} WHERE id = {id_account} ;')
        conn.commit()
        print('Income was added!')
    except:
        print('Error!')


def valid_money(id_account, amount):
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT balance FROM card WHERE id = {id_account} ;')
        conn.commit()
    except:
        print('Error!')

    for c in cur.fetchall():
        balance = c[0]

    if balance >= amount:
        return True

    print('Not enough money!')
    return False


def transfer(id_account, card_number, amount):
    cur = conn.cursor()
    try:
        cur.execute(f'UPDATE card SET balance = balance - {amount} WHERE id = {id_account} ;')
        conn.commit()
    except:
        print('Error!')

    cur = conn.cursor()
    try:
        cur.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {card_number} ;')
        print('Success!')
        conn.commit()
    except:
        print('Error!')

def do_transfer(id_account):
    print('\nTransfer\nEnter card number:')
    card_number = input()

    if card_number != algorithm_lunh(card_number):
        print('\nProbably you made mistake in the card number. Please try again!')
    elif not valid_card(card_number):
        print('Enter how much money you want to transfer:')
        amount = int(input())
        if valid_money(id_account, amount):
            transfer(id_account, card_number, amount)
    else:
        print('Such a card does not exist.')

def close_account(id_account):
    cur = conn.cursor()
    try:
        cur.execute(f'DELETE FROM card WHERE id = {id_account} ;')
        conn.commit()
        print('\nThe account has been closed!')
        return True
    except:
        return False
        print('Error!')


def create_tables():  # crea la tabla en caso que no exista
    cur = conn.cursor()
    try:
        cur.execute(''
                    'CREATE TABLE IF NOT EXISTS card('
                    'id INTEGER, '
                    'number TEXT, '
                    'pin TEXT, '
                    'balance INTEGER DEFAULT 0);')
        # cur.execute('DROP TABLE card;')
        ret = True
    except:
        ret = False
    # After doing some changes in DB don't forget to commit them!
    conn.commit()
    return ret


def valid_card(id_card):
    valid = True
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT * FROM card WHERE number = {id_card} ;')
    except:
        valid = True
    for c in cur.fetchall():
        if c[0] != 0:
            valid = False
    conn.commit()
    return valid


def insert_card(number_card, password):
    cont = id_card()
    cur = conn.cursor()
    cur.execute(f'INSERT INTO card (id, number, pin) values({cont},{number_card},{password})')
    conn.commit()


def id_card():
    cur = conn.cursor()
    cur.execute(f'SELECT IFNULL(MAX(id),0) FROM card;')
    for c in cur.fetchall():
        cont = c[0]
    conn.commit()
    return cont + 1


def select_card():
    cur = conn.cursor()
    cur.execute(f'SELECT id, number, pin, balance FROM card;')
    for c in cur.fetchall():
        print(c)
    conn.commit()


def valid_login(card_number, password):
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT id number FROM card WHERE number = {card_number} and pin = {password};')
    except:
        valid = False
    finally:
        valid = False
    for c in cur.fetchall():
        valid = c[0]
    conn.commit()
    return valid


def algorithm_lunh(card):
    double_sum, check_sum, new_card = [], [], []

    for i in range(0, len(card) - 1):
        new_card.append(card[i])
        if i % 2 == 0:
            double_sum.append(str(int(card[i]) * 2))
        else:
            double_sum.append(card[i])

    for x in double_sum:
        check_sum.append(sum([int(i) for i in x]))

    if (sum(check_sum) + int(str(sum(check_sum) * 9)[-1])) % 10 == 0:
        new_card.append(str(sum(check_sum) * 9)[-1])
        return ''.join(new_card)
    return None


def generator_account():
    new_card, password = ["400000"], []  # 6
    for x in range(5):  # 10
        new_card.append(str(random.randint(10, 99)))  # 10

    _new_card = algorithm_lunh(''.join(new_card))

    if valid_card(_new_card):
        for x in range(4):  # 4
            password.append(str(random.randint(0, 9)))  # 4
        insert_card(''.join(_new_card), ''.join(password))
        print("\nYour card has been created")
        print(f"Your card number:\n{''.join(_new_card)}")
        print(f"Your card PIN:\n{''.join(password)}")
        return True
    return False


def create_account():
    while True:
        if generator_account():
            break


def menu_principal():
    print("\n1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def menu_user():
    print("\n1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


def valid_account():
    card = input('\nEnter your card number:\n',)
    password = input('Enter your PIN:\n',)
    return valid_login(card, password)


def transactions(id_account, opcion):
    if opcion == 1:
        show_balance(id_account)
    elif opcion == 2:
        add_income(id_account)
    elif opcion == 3:
        do_transfer(id_account)


# -----------------------
# person = Client()
resp, resp2 = -1 , -1
create_tables()  # creacion de tablas
# select_card()

while resp != 0:
    menu_principal()
    resp = int(input())
    if resp == 1:
        create_account()
    elif resp == 2:
        id = valid_account()
        if id != False:
            print('\nYou have successfully logged in!')
            while resp2 != 0:
                menu_user()
                resp2 = int(input())
                if resp2 in (1, 2, 3):
                    transactions(id, resp2)
                elif resp2 == 4:
                    if close_account(id):
                        break
                elif resp2 == 5:
                    print("\nYou have successfully logged out!")
                    break
                elif resp2 == 0:
                    resp = 0
        else:
            print('\nWrong card number or PIN!')

if resp == resp2 == 0:
    print("\nBye!")
    conn.close()
