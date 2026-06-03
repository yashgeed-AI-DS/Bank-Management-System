import json 
import random 
import string
from pathlib import Path 

class Bank:
    database = "database.json"   #json file which store data
    data = []  # it is a dami file which is store json data copy 

    if Path(database).exists():
        with open (database) as fs:
            data = json.loads(fs.read())   # it is store data in json whenever the class is call 
    
    @classmethod
    def __update(cls):
        with open(cls.database,"w") as fs:
            fs.write(json.dumps(cls.data))

    @classmethod
    def __generate_account_no(cls):
        alpha = random.choices(string.ascii_letters, k = 8)
        num = random.choices(string.digits , k = 4 )
        acc = alpha + num 
        random.shuffle(acc)
        return "".join(acc)
    
    def creat_user(self):
        info = {
            "name" : input("Enter user name:-"),
            "age" : int(input("Enter user Age:-")),
            "email" : input("Enter user Email:-"),
            "AccountNO." : Bank.__generate_account_no(),
            "pin" : int(input("Enter user pin:-")),
            "balance" : 0
        }
        if  info["age"] < 12 :
            print("Sorry cannot creeate account , your are not eligible")
        elif len(str(info["pin"])) != 4:
            print("pin is invalid, Try again!")
        else:
            Bank.data.append(info)
            Bank.__update()
        
    def deposit(self):
        accno = input("Enter your account number:-")
        pin = int(input("Enter your pin:-"))
        userdata = [i for i in Bank.data if i ["AccountNO."] == accno and i["pin"] == pin]
        if userdata == False:
            print("Sorry invalid account number or pin")
        else:
            amount = int(input("Enter the amount you want to deposit:-"))
            userdata[0]["balance"]+= amount
            Bank.__update()
            print("Balance Added successfully")

    def withdraw_money(self):
        accno = input("Enter your account number:-")
        pin = int(input("Enter your pin:-"))
        userdata = [i for i in Bank.data if i ["AccountNO."] == accno and i["pin"] == pin]
        if userdata == False:
            print("Sorry invalid account number or pin")
        else:
            amount = int(input("Enter the amount you want to withdraw:-"))
            if amount > userdata[0]["balance"]:
                print("Sorry insufficient balance")
            else:
                userdata[0]["balance"]-= amount
                Bank.__update()
                print("Balance withdrawn successfully")
    def show_details(self):
        accno = input("Enter your account number:-")
        pin = int(input("Enter your pin :-"))
        userdata = [i for i in Bank.data if i ["AccountNO."]== accno and i["pin"]== pin]
        if not userdata :
            print("NO data found!")
        else:
            for i in userdata[0]:
                print(f"{i} - {userdata[0][i]}")
        
    def update_details(self):
        accno = input("Enter your account number:-")
        pin = int(input("Enter your pin :-"))
        userdata = [i for i in Bank.data if i ["AccountNO."]== accno and i["pin"]== pin]
        if userdata == False:
            print("No data found!")
        else:
            print("You cannot change your balance ,account number and age")
            
            newdata = {
                "name" : input("Enter your new name or press enter to skip :-"),
                "email" : input("Enter your new email or press enter to skip:-"),
                "pin" : input("Enter your new pin or press enter to skip:-")
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]["name"]
            if newdata["email"] == "":
                newdata["email"] = userdata[0]["email"]
            if newdata["pin"] == "":
                newdata['pin'] = str(userdata[0]["pin"])

            for i in userdata[0]:
                if i in newdata and i != "pin":
                    userdata[0][i] = newdata[i]
                if i == "pin":
                    userdata[0][i] = int(newdata[i])
            Bank.__update()
            print("Details updated successfully")
    
    def delete_user(self):
        accno = input("Enter your account number:-")
        pin = int(input("Enter your pin :-"))
        userdata = [i for i in Bank.data if i ["AccountNO."]== accno and i["pin"]== pin]
        if userdata == False:
            print("No data found!")
        else:
            print("Are you sure you want to delete your account? (Yes/No)")
            check = input("Enter your response:-")
            if check.lower() == "yes":
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)

                Bank.__update()
                print("Account deleted successfully")

bank = Bank()

while True:
    print("Press 1 for creating an account")
    print("Press 2 for depositing money")
    print("Press 3 for withdrawing money")
    print("Press 4 for details of a user")
    print("Press 5 for updating users details ")
    print("Press 6 for deleting user")

    res = int(input("Tell your response:-"))
    if res == 1:
        bank.creat_user()
    elif res == 2:
        bank.deposit()
    elif res == 3:
        bank.withdraw_money()
    elif res == 4:
        bank.show_details()
    elif res == 5:
        bank.update_details()
    elif res == 6:
        bank.delete_user()
    elif res == 0:
        break
    else:
        print("Invalid response, Try again!")