import sqlite3
import re
from prettytable import PrettyTable


class DB_connect:
    def __init__(self):  # constructor
        # database name of flight booking Name
        try:
            db_name = "flight-DB-python"
            self.connect = sqlite3.connect(db_name)
            self.cursor = self.connect.cursor()

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_credential (email TEXT,name TEXT,passwd TEXT,dob DATE,
            type INTEGER)''')
            self.connect.commit()
        except sqlite3.Error as Err:
            self.connect.rollback()
            print("Database Error : ", Err)


# Admin Work Space
# class Admin():
#
#
# # User Work Space
# class User():
#
#
# class FlightbookApp(Admin,User):
#     def __init__(self,user_data):
#         self.user_data = user_data



class Login_module(DB_connect):
    def __init__(self):
        super().__init__()

    @staticmethod
    def encrypt(text, key):
        return ''.join([chr(ord(char) ^ key) for char in text])

    def validate_date(self, dob):
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not bool(re.match(date_pattern, dob)):
            return False
        else:
            year = int(dob[0:4])
            mon = int(dob[5:7])
            date = int(dob[8::])
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                if mon == 2:
                    return True if 29 >= date > 0 else False
            else:
                if mon == 2:
                    return True if 28 >= date > 0 else False
            if mon % 2 == 0:
                if 7 > mon > 0 and 0 < date < 31:
                    return True
                elif 13 > mon > 7 and 0 < date <= 31:
                    return True
            else:
                if 0 < mon <= 7 and 0 < date <= 31:
                    return True
                elif 13 > mon > 8 and 0 < date < 31:
                    return True
            return False

    @property
    def signup(self):

        details = []
        interrupt = False
        print("Enter 0 Anywhere to Exit")
        while True and not interrupt:
            u_name = input("Enter UserName >> ")
            if u_name == '0':
                interrupt = True
            else:
                details.append(u_name)
                break

        while True and not interrupt:
            email = input("Enter Email >> ")
            if email == 0:
                interrupt = True
                break
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if re.match(email_regex, email):
                try:
                    self.cursor.execute('SELECT count(*) FROM user_credential WHERE email = ? ', (email,))
                except sqlite3.Error as error:
                    self.connect.rollback()
                    print("Database Error : ", error)
                    interrupt = True

                info = self.cursor.fetchall()
                print(info)
                if not info[0][0]:
                    details.append(email)
                else:
                    print("Email Already Registered !")
                    continue
                break
            else:
                print("Not Valid Email")
        while True and not interrupt:
            pas_wd = input("Enter PassWord >> ")
            pas_wd.strip()
            if pas_wd == '0':
                interrupt = True
                break
            pwd_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

            match = re.match(pwd_pattern, pas_wd)

            if match and details[0] != pas_wd:
                details.append(pas_wd)
                break
            else:
                print("Invalid Password,Try another")
        while True and not interrupt:
            dob = input("Enter DOB: yyyy-MM-dd >> ")
            if dob == '0':
                interrupt = True
                break

            if self.validate_date(dob):
                details.append(dob)
                break
            else:
                print("Not Valid Date")
        while True and not interrupt:
            u_a = input("Enter 1 for Admin (or) 2 for User >> ")
            if u_a == '0':
                interrupt = True
                break
            if u_a == '1':
                details.append(1)
                break
            elif u_a == '2':
                details.append(2)
                break
            else:
                continue

                # Now insert or create the record in the table
        if not interrupt:

            details[2] = self.encrypt(details[2], len(details[2]))
            # details = [ username , email ,password, dob, admin/user ]
            # table = mail TEXT,name TEXT,passwd TEXT,dob DATE, type INTEGER
            try:
                self.cursor.execute("INSERT INTO user_credential VALUES (?, ?, ?, ?, ?)",
                                    (details[1], details[0], details[2], details[3], details[4]))
                self.connect.commit()
                return True
            except sqlite3.Error as error:
                self.connect.rollback()
                print("Database Error :", error)
                print("DB_connection is failed please refer in Internet")
                return False
        else:
            return False

    def login(self):
        print("Enter 0 Anywhere to Exit")
        pwd_changed = False
        forgot_pwd_flag = False
        while True:

            given_email = input("Enter Email Id >> ")
            if given_email == '0':
                return -1
            else:
                given_pwd = input("Enter Password >> ")
                try:
                    self.cursor.execute("select count(*),passwd,name,type,email from user_credential where email = ?",
                                        (given_email,))
                except sqlite3.Error as err:
                    print("Database Error on find User : ", err)
                    return -1
                info_query = self.cursor.fetchall()
                if info_query[0][0] == 0:
                    print("User Not Found!")
                    continue
                if self.encrypt(given_pwd, len(given_pwd)) == info_query[0][1]:
                    return info_query[0][2::]
                else:
                    change_pwd_choice = input("Invalid Password!\nDue Want to Reset Password Press 0 else 1 >> ")
                    if change_pwd_choice == '1':
                        continue
                    if change_pwd_choice == '0':
                        while True:
                            new_pwd = input("Enter New Password >> ")
                            pwd_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

                            if bool(re.match(pwd_pattern, new_pwd)):
                                try:
                                    self.cursor.execute(
                                        "UPDATE user_credential SET passwd = ? where email = ?",
                                        (self.encrypt(new_pwd, len(new_pwd)), given_email)
                                    )
                                    self.connect.commit()
                                    print("Password Changed !")
                                    break
                                except sqlite3.Error as err:
                                    self.connect.rollback()
                                    print("DB Error : ", err)
                            else :
                                print("Invalid Password, Try Again ")
                                continue


if __name__ == "__main__":

    print('''#--------------------------------------------------
#--------------FLIGHT BOOKING SYSTEM---------------
#__________________________________________________''')
    while True:
        user_choice = int(input("Hi, Choose :\nSign Up : 1 (or) Sign In : 2 >> "))
        login = Login_module()
        if user_choice == 1:
            if login.signup:
                print("Successfully Sign Up")
            else:
                print("Please Try again")
                continue
        if user_choice == 2:
            user_details = login.login()
            if user_details == -1:
               continue
            # FlightAPP = FlightbookApp(user_details)


