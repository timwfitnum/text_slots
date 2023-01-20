"""Main file to handle text based slot game!"""

import random

MAX_LINES = 5
MAX_BET = 100
MIN_BET = 1
COLS = 5

SYMBOLS_COUNT = {
    "A": 2,
    "B": 4,
    "C": 7,
    "D": 11,
    "E": 16
}

SYMBOLS_VALUE = {
    "A": 16,
    "B": 11,
    "C": 7,
    "D": 4,
    "E": 2
}

def get_slot_machine_spin(rows, cols, symbols):
    """Get slot machine symbols."""
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    """Print transposed columns to show them as rows."""
    print()
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            print(column[row], " | " if i!= len(columns) -1 else "\n", end="")
    print()

def get_winnings(columns, lines, bet, values):
    """Calculate winnings, if any."""
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line+1)
    return winnings, winning_lines


def deposit():
    """Def to handle and validate deposit."""
    while True:
        amount = input("What would you like to deposit? :$")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Please enter a number greater than 0.")
        else:
            print("Please enter a number greater than 0.")
    return amount

def get_number_of_lines():
    while True:
        lines = input(f"Enter number of lines to bet on (1-{MAX_LINES})? :")
        if lines.isdigit():
            lines = int(lines)
            if 0 < lines <= MAX_LINES:
                break
            else:
                print("Please enter a valid number of lines!")
        else:
            print("Please enter a valid number of lines!")
    return lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? :$")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET<=amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}!")
        else:
            print("Please enter a number between ${MIN_BET} - ${MAX_BET}!")
    return amount

def get_valid_bet(balance, lines):
    while True:
        bet = get_bet()
        if bet * lines > balance.get():
            print(f"You do not have enough to bet that amount, your current balance is {balance.get()}.")
        else:
            return bet


def slot_spin(balance, previous_bet = None):
    """Handle each slot spin and rebet."""
    if previous_bet:
        lines = previous_bet[0]
        bet = previous_bet[1]
    else:
        lines = get_number_of_lines()
        bet = get_valid_bet(balance, lines)
    return spin(lines, bet)

def spin(lines, bet):
    """Does the spin calculation."""
    total_bet = bet * lines
    print(f"You are betting {bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(lines, COLS, SYMBOLS_COUNT)
    print_slot_machine(slots)
    winnings, winning_lines = get_winnings(slots, lines, bet, SYMBOLS_VALUE)
    if winnings > 0:
        print(f"You have won ${winnings} on lines: {winning_lines}.")
    else:
        print("You did not win!")
    return winnings - total_bet, [lines, bet]

def rebet_spin(balance, lines, bet):
    rebet = ""
    while balance.get() >= lines*bet and rebet.lower() != "n" :
        print(f"Your current balance is ${balance.get()}")
        rebet = input(f"Would you like to rebet? {bet}$ on {lines} lines! (Y/N)")
        if rebet.lower() == "y":
            losses = slot_spin(balance, [lines, bet])[0]
            balance.set_new_balance(losses)
        else:
            return False

class Balance:
    def __init__(self, balance):
        self.balance = balance
        self.deposited = balance
    
    def set_new_balance(self,losses):
        self.balance += losses
        
    def get(self):
        return self.balance

    def add_new_deposit(self, amount):
        self.deposited += amount
        self.balance += amount



def main():
    """Def to make game replayable."""
    balance = Balance(deposit())
    while True:
        print(f"Current balance is ${balance.get()}")
        
        spin = input("Press enter to play, d to deposit (q to quit).")
        if spin == "q":
            break
        if spin.lower() == "d":
            balance.add_new_deposit(deposit())
        
        slot_result = slot_spin(balance)
        balance.set_new_balance(slot_result[0])
        previous_bet = slot_result[1]
        
        if balance.get() >= previous_bet[0] * previous_bet[1]:
            rebet_spin(balance, previous_bet[0], previous_bet[1])
        keep_rebetting = True
        deposit_needed = not bool(balance.get())
        while True and deposit_needed:
            if balance.get() == 0:
                print("Current balance is $0")
                deposit_more = input("Please deposit more to play! q to quit!")
                if deposit_more == "q":
                    print(f'You left with ${balance.get()}. You {"won" if balance.deposited <= balance.get() else "lost"} ${abs(balance.get() - balance.deposited)}')
                    exit()
                balance.add_new_deposit(deposit())
            if balance.get() >= previous_bet[0] * previous_bet[1] and keep_rebetting:
                keep_rebetting = rebet_spin(balance, previous_bet[0], previous_bet[1])
            else:
                break

    print(f'You left with ${balance.get()}. You {"won" if balance.deposited <= balance.get() else "lost"} ${abs(balance.get() - balance.deposited)}')
main()