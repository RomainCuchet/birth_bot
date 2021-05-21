import functions

functions.create_birthday_tab()
while contitue := str(input("Enregistrer un autre anniversaire (yes/no) ? ")) == "yes":
    first_name, name, birth_date_year, birth_date_month_day = functions.collect_information()
    functions.insert_birthday(first_name, name, birth_date_year, birth_date_month_day)