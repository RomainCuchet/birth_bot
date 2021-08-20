import functions as f
f.create_birthday_tab()
while command := str(input('Add a new birthday event ? (yes/no) : ')) == 'yes':
    first_name, name, birth_date_year, birth_date_month_day = f.collect_information()
    f.insert_birthday(first_name, name, birth_date_year, birth_date_month_day)
print('Now the database is even stronger !')