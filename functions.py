# After the creation of your Vonage's accont change key and secrets value (set at "") with your own data

import sqlite3
import datetime
import re
import vonage

test = False
if not test:
    data_base = sqlite3.connect('birth_bot-data')
else:
    data_base = sqlite3.connect('test-data')
cursor = data_base.cursor()


def create_birthday_tab():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people(
         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
         name TEXT,
         first_name TEXT,
         birth_date_year INT,
         birth_date_month_day TEXT
         )
    """)


def collect_information():
    first_name = str(input("Prénom : "))
    name = str(input("Nom : "))
    day = re.sub('0', '', str(input("Jour : ")))
    month = re.sub('0', '', str(input("Mois : ")))
    birth_date_year = int(input("Année : "))
    birth_date_month_day = "{month}-{day}".format(month=month, day=day)
    return first_name, name, birth_date_year, birth_date_month_day


def insert_birthday(first_name, name, birth_date_year, birth_date_month_day):
    data = {"first_name": first_name, "name": name, "birth_date_year": birth_date_year,
            "birth_date_month_day": birth_date_month_day}
    save = str(input("Sauvegarder ? (oui/non : )"))
    if save == "oui":
        if is_registered(first_name, name):
            print("{first_name} {name} est déjà dans la base !".format(first_name=first_name, name=name))
        else:
            data_base.execute("""
                INSERT INTO people(first_name, name, birth_date_year, birth_date_month_day) 
                VALUES(:first_name, :name, :birth_date_year, :birth_date_month_day)""", data)
            data_base.commit()
            print("{first_name} {name} entre dans la base !".format(first_name=first_name, name=name))
    else:
        print("opération annulée")


def get_birthday(birth_date_month_day):
    cursor.execute("""SELECT first_name, name , birth_date_year, birth_date_month_day
                    FROM people WHERE birth_date_month_day=?""", (birth_date_month_day,))
    response = cursor.fetchall()
    return response


def is_registered(first_name, name):
    cursor.execute("""SELECT first_name, name , birth_date_year, birth_date_month_day
                    FROM people WHERE first_name=? AND name=?""",
                   (first_name, name,))
    response = cursor.fetchone()
    if response is not None:
        return True
    else:
        return False


def birth_bot_update():
    date = datetime.datetime.now()
    birth_date_month_day = "{month}-{day}".format(month=date.month, day=date.day)
    birthdays = get_birthday(birth_date_month_day)
    if len(birthdays) > 0:
        for i in birthdays:
            send_message(i[0], i[1], i[2], i[3])
    else:
        print("No birthday today !")


def send_message(first_name, name, birth_date_year, birth_date_month_day):
    age = datetime.datetime.now().year - birth_date_year
    date = birth_date_month_day.split('-')
    if len(date[0]) < 2:
        month = '0' + date[0]
    else:
        month = date[0]
    if len(date[1]) < 2:
        day = '0' + date[1]
    else:
        day = date[1]
    birth_date = "{day}/{month}".format(day=day, month=month)
    text = " {birth_date} \n c'est l'anniversaire de {first_name} {name}. Déja {age}ans !".format(birth_date=birth_date,
                                                                                                  first_name=first_name,
                                                                                                  name=name, age=age)
    client = vonage.Client(key="", secret="")
    sms = vonage.Sms(client)
    response_data = sms.send_message(
        {
            "from": "Birth_bot",
            "to": "33638979646",
            "text": text,
        }
    )

    if response_data["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {response_data['messages'][0]['error-text']}")
