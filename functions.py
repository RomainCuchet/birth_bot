# -*- coding: utf-8 -*-
import sqlite3
import datetime
import re
import smtplib
from email.message import EmailMessage

""" Gmail automatically switch off the 'Autoriser les applications moins sécurisées.'
    If the mail isn't send change it """ 
gmail_user = 'birthbotpython@gmail.com'
gmail_password = 'mgh15/qv'
gmail_rec = 'romain.cuchet02@gmail.com'

test = False
# enable to use different data base for test
if not test:
    data_base = sqlite3.connect('birth_bot-data')
else:
    data_base = sqlite3.connect('test-data')
cursor = data_base.cursor()


def create_birthday_tab():
    """ create a new table into the database which represents a birthday event """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people(
         name TEXT,
         first_name TEXT,
         birth_date_year INT,
         birth_date_day_month TEXT
         )
    """)

create_birthday_tab()


def collect_information():
    """ collect required information to create a birthday event  """
    first_name = str(input("Prénom : "))
    name = str(input("Nom : "))
    day = re.sub('0', '', str(input("Jour : ")))
    month = re.sub('0', '', str(input("Mois : ")))
    birth_date_year = int(input("Année : "))
    birth_date_month_day = "{day}/{month}".format(month=month, day=day)
    return first_name, name, birth_date_year, birth_date_month_day


def insert_birthday(first_name, name, birth_date_year, birth_date_day_month):
    """ add a birthday event to the specified database """
    data = {"first_name": first_name, "name": name, "birth_date_year": birth_date_year,
            "birth_date_day_month": birth_date_day_month}
    save = str(input("Sauvegarder ? (oui/non : )"))
    if save == "oui":
        if is_registered(first_name, name):
            print("{first_name} {name} est déjà dans la base !".format(first_name=first_name, name=name))
        else:
            data_base.execute("""
                INSERT INTO people(first_name, name, birth_date_year, birth_date_month_day) 
                VALUES(:first_name, :name, :birth_date_year, :birth_date_day_month)""", data)
            data_base.commit()
            print("{first_name} {name} entre dans la base !".format(first_name=first_name, name=name))
    else:
        print("opération annulée")


def get_birthday(birth_date_day_month):
    """ search and collect birthday event from the database with the birth_date_day_month argument"""
    cursor.execute("""SELECT first_name, name , birth_date_year, birth_date_day_month
                    FROM people WHERE birth_date_day_month=?""", (birth_date_day_month,))
    response = cursor.fetchall()
    return response


def get_all_birthday():
    cursor.execute(""""SELECT * FROM people""")
    response = cursor.fetchall()
    return response


def is_registered(first_name, name):
    """ test if someone's birthday is already registered into the database, return true or false"""
    cursor.execute("""SELECT first_name, name , birth_date_year, birth_date_day_month
                    FROM people WHERE first_name=? AND name=?""",
                   (first_name, name,))
    response = cursor.fetchone()
    if response is not None:
        return True
    else:
        return False


def birth_bot_update():
    """ the function run every day. Collects the birthday event of the day and send them to the specified email  """
    date = datetime.datetime.now()
    birth_date_day_month = "{day}/{month}".format(month=date.month, day=date.day)
    birthdays = get_birthday(birth_date_day_month)
    if len(birthdays) > 0:
        for i in birthdays:
            send_mail(gmail_user, gmail_password, gmail_rec, create_message(i))
    else:
        send_mail(gmail_user, gmail_password, gmail_rec, 'No birthday today :)')


def send_mail(gmail_user, gmail_password, gmail_rec, message):
    mail = EmailMessage()
    mail['Subject'] = "birthday event"
    mail['From'] = gmail_user
    mail['To'] = gmail_rec
    mail.set_content(message)

    # Send the message via our own SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.send_message(mail)
    server.quit()


def create_message(birthday_event):
    """ create the message string to send for a birth event"""
    message = ("{0} | Today it's {1} {2} birthday ! ".format(birthday_event[3], birthday_event[0], birthday_event[1]))
    if type(birthday_event[2]) is int:
        date = datetime.datetime.now()
        message += " Already {0} years old ! ".format(date.year - birthday_event[2])
    return message


if __name__ == '__main__' :
    birth_bot_update()
