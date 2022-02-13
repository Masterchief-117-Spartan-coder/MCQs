import mysql.connector
from datetime import date
import time


def sql_control_center(var_name="UNKNOWN", var_score="0", test_type="UNKNOWN", retrive=False, date=date.today(),
                       row_number=1):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="1234"
    )

    print(mydb)
    mycursor = mydb.cursor()
    mycursor.execute("show databases;")
    databases_list = mycursor.fetchall()
    print(databases_list, var_name)
    print((var_name.lower(), ) in databases_list)
    if (var_name.lower(), ) in databases_list:
        mycursor.execute(f'use {var_name.lower()};')
    else:
        mycursor.execute(f"create database {var_name.lower()};")
        mycursor.execute(f'use {var_name.lower()};')
        mycursor.execute("create table score_board("
                         "id INT AUTO_INCREMENT PRIMARY KEY, "
                         f"Test_type varchar(255) NOT NULL,"
                         f" Score int,"
                         f"date_of_submission DATE NOT NULL);")

        time.sleep(6)

    if not retrive:
        # mycursor.execute('desc score_board;')
        # print(mycursor.fetchall())
        sql = "INSERT INTO score_board (Test_type, Score, date_of_submission) VALUES (%s, %s, %s)"
        val = (test_type, var_score, date.today())
        mycursor.execute(sql, val)
        mydb.commit()

    if retrive:
        # mycursor.execute('ALTER TABLE score_board ADD FULLTEXT(Test_type);')
        mycursor.execute('select *'
                         'from score_board '
                         f"WHERE Test_type LIKE '{test_type}%';")
        # print(mycursor.fetchall())
        return mycursor.fetchall()  # TODO: limit of rows...

# sql_control_center("Ishan", test_type="Physics", retrive=True)
