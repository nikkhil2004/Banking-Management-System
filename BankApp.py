import json
import random
import string
from pathlib import Path
import streamlit as st


class Bank:
    database = "data.json"
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            data = []
    except Exception as err:
        st.error(f"Exception: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data, indent=4))

    @classmethod
    def __accnumgenerator(cls):
        alpha = random.choices(string.ascii_letters, k=4)
        num = random.choices(string.digits, k=2)
        spchar = random.choices("!@#*", k=2)
        return "".join(alpha + num + spchar)

    def createaccount(self, name, age, email, pin):
        info = {
            "account_number": Bank.__accnumgenerator(),
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "balance": 0
        }

        if age < 18 or len(str(pin)) != 4:
            return None, "Age must be ≥18 and PIN must be 4 digits"
        else:
            Bank.data.append(info)
            Bank.__update()
            return info, "Account created successfully!"

    def deposit(self, account_number, pin, amount):
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        if not userdata:
            return "Account not found"
        if amount > 10000 or amount <= 0:
            return "Amount must be between 1 and 10000"
        userdata[0]['balance'] += amount
        Bank.__update()
        return f"₹{amount} deposited successfully. New Balance: ₹{userdata[0]['balance']}"

    def withdraw(self, account_number, pin, amount):
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        if not userdata:
            return "Account not found"
        if amount > userdata[0]['balance'] or amount <= 0:
            return "Insufficient balance or invalid amount"
        userdata[0]['balance'] -= amount
        Bank.__update()
        return f"₹{amount} withdrawn successfully. Remaining Balance: ₹{userdata[0]['balance']}"

    def details(self, account_number, pin):
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        if not userdata:
            return None
        return userdata[0]

    def update(self, account_number, pin, new_email=None, new_pin=None):
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        if not userdata:
            return "Account not found"

        if new_email:
            userdata[0]['email'] = new_email
        if new_pin:
            if len(str(new_pin)) == 4:
                userdata[0]['pin'] = new_pin
            else:
                return "PIN must be 4 digits"

        Bank.__update()
        return "Account updated successfully!"

    def delete(self, account_number, pin):
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        if not userdata:
            return "Account not found"
        Bank.data.remove(userdata[0])
        Bank.__update()
        return "Account deleted successfully!"


st.set_page_config(page_title="Banking Management System", page_icon="🏦", layout="centered")

st.title("🏦 Banking Management System")
st.write("Welcome to OOP-based banking app!")

bank = Bank()

menu = ["Create Account", "Deposit", "Withdraw", "View Details", "Update Account", "Delete Account"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, step=1)
    email = st.text_input("Enter your email")
    pin = st.number_input("Set a 4-digit PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Create Account"):
        info, msg = bank.createaccount(name, age, email, pin)
        if info:
            st.success(msg)
            st.json(info)
        else:
            st.error(msg)

elif choice == "Deposit":
    st.subheader("Deposit Money")
    acc = st.text_input("Enter account number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)
    amt = st.number_input("Enter amount", min_value=1, step=1)

    if st.button("Deposit"):
        st.info(bank.deposit(acc, pin, amt))

elif choice == "Withdraw":
    st.subheader("Withdraw Money")
    acc = st.text_input("Enter account number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)
    amt = st.number_input("Enter amount", min_value=1, step=1)

    if st.button("Withdraw"):
        st.info(bank.withdraw(acc, pin, amt))

elif choice == "View Details":
    st.subheader("Account Details")
    acc = st.text_input("Enter account number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Get Details"):
        details = bank.details(acc, pin)
        if details:
            st.json(details)
        else:
            st.error("Account not found")

elif choice == "Update Account":
    st.subheader("Update Account")
    acc = st.text_input("Enter account number")
    pin = st.number_input("Enter current PIN", min_value=1000, max_value=9999, step=1)
    new_email = st.text_input("Enter new email (optional)")
    new_pin = st.text_input("Enter new 4-digit PIN (optional)")

    if st.button("Update"):
        new_pin_val = int(new_pin) if new_pin.strip() else None
        msg = bank.update(acc, pin, new_email if new_email.strip() else None, new_pin_val)
        if "successfully" in msg:
            st.success(msg)
        else:
            st.error(msg)

elif choice == "Delete Account":
    st.subheader("Delete Account")
    acc = st.text_input("Enter account number")
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Delete"):
        st.warning(bank.delete(acc, pin))
