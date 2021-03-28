import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card(id INTEGER,number TEXT,
                                                pin TEXT,balance INTEGER DEFAULT 0);''')
conn.commit()
bank_account_list = dict()
exit_main = False
main_message = ["1. Create an account", "2. Log into account", "0. Exit"]
account_message = ['''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''']

cur.execute('SELECT * FROM card')
cards_info = cur.fetchall()

a = 0
def generate_account():
    global cards_info
    global bank_account_list
    global balance
    global a
    balance = 0
    a += 1
    card_number = 400000000000000 + random.randint(0, 999999999)
    card_number = card_number * 10 + luhn_checksum(card_number)
    pin = random.randint(1000, 9999)
    bank_account_list.update({card_number: {'pin': '{0:04d}'.format(pin), 'balance': 0}})
    for_db = []
    for_db.append(a)
    for_db.append(card_number)
    for_db.append(pin)
    for_db.append(balance)
    cur.execute('INSERT INTO card VALUES(?,?,?,?)',for_db)
    conn.commit()
    cur.execute('SELECT * FROM card')
    cards_info = cur.fetchall()
    return card_number

def create_account():
    print("Your card has been created")
    print("Your card number:")
    card_number = generate_account()
    print(card_number)
    print("Your card PIN:")
    print(bank_account_list[card_number]['pin'])


def luhn_checksum(card_number):
    _numbers = list(map(int, str(card_number)))
    for i in range(0, 15, 2):
        x = _numbers[i] * 2
        _numbers[i] = x if x < 10 else x - 9
    _sum = sum(_numbers)
    return 0 if _sum % 10 == 0 else 10 - _sum % 10



def log_into_account():
    global cards_info
    global b
    global spisok
    spisok = []
    b = 0
    print("Enter your card number:")
    card_number = input()
    print("Enter your PIN")
    pin = input()
    for i in range(len(cards_info)):
        if card_number in cards_info[b][1] and pin in cards_info[b][2]:
            print("You have successfully logged in!")
            account_menue(card_number)
            return True
        else:
            b += 1
    print("Wrong card number or PIN!")
    


def account_menue(card_number):
    global exit_main
    global cards_info
    c = 0
    for_delete = []
    check_sum = 0
    spisok = []
    cards_number = []
    for p in range(0,len(cards_info),1):
        cards_number.append(cards_info[p][1])
    while True:
        print('\n'.join(account_message))
        choose_account = int(input())
        if choose_account == 0:
            exit_main = True
            break
        elif choose_account == 1:
            print("Balance: " + str(cards_info[b][3]))
        elif choose_account == 2:
            print("Enter income:")
            income = int(input())
            spisok.append(income)
            spisok.append(card_number)
            cur.execute('UPDATE card SET balance = balance+(?) WHERE number = (?)',spisok)
            conn.commit()
            print("Income was added!")
        elif choose_account == 3:
            print("Transfer\nEnter card number:")
            number = input()
            check_sum = 0
            for i in range(0,len(number),2):
                check = int(number[i]) * 2
                if check > 9:
                    check -= 9
                    check_sum += check
                else:
                    check_sum += check
            for m in range(1,len(number),2):
                check_sum += int(number[m])
            if check_sum % 10 != 0:
                print("Probably you made mistake in the card number. Please try again!")
            elif number == card_number:
                print("You can't transfer money to the same account!")
            elif number not in cards_number:
                print("Such a card does not exist.")
            else:
                print("Enter how much money you want to transfer:")
                transfer = int(input())
                if transfer > cards_info[b][3]:
                    print("Not enough money!")
                else:
                    spisok.append(transfer)
                    spisok.append(number)
                    cur.execute('UPDATE card SET balance = balance+(?) WHERE number = (?)',spisok)
                    conn.commit()
                    spisok = []
                    spisok.append(transfer)
                    spisok.append(cards_info[b][1])
                    cur.execute('UPDATE card SET balance = balance - (?) WHERE number = (?)',spisok)
                    conn.commit()
                    print("Success!")
        elif choose_account == 4:
            for_delete.append(card_number)
            cur.execute('DELETE FROM card WHERE number = (?)',for_delete)
            conn.commit()
            print("The account has been closed!")
            return None
        elif choose_account == 5:
            print("You have successfully logged out!")
            return None
                    

while True:
    print('\n'.join(main_message))
    choose_main = int(input())
    if choose_main == 0:
        exit_main = True
    elif choose_main == 1:
        create_account()
    elif choose_main == 2:
        log_into_account()
    if exit_main:
        print("Bye!")
        break