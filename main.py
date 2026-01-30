from cryptography.fernet import Fernet
import os

# 
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    return open("secret.key", "rb").read()

key = load_key()
fer = Fernet(key)

def view():
    if not os.path.exists('passwords.txt'):
        print("\n[!] ")
        return
    print("\n---  ---")
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            if "|" not in data: continue
            user, passw = data.split("|")
            print(f"Account: {user} | Password: {fer.decrypt(passw.encode()).decode()}")

def add():
    name = input('\account name): ')
    pwd = input("পাসওয়ার্ড দিন: ")
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()
    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + encrypted_pwd + "\n")
    print("[+] SUCCESSFULLY SAVED!")

print("========================================")
print("   WELCOME TO PASSWORD MANAGER")
print("========================================")

while True:
    mode = input("\n add new password 'add', show your password 'view', quit 'q' write: ").lower()
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("rong input try again।")