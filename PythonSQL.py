import mysql.connector
from datetime import date, datetime, timedelta
from mysql.connector import Error
import pandas as pd
import xlrd
import openpyxl
import matplotlib.pyplot as plt

try:
    connection = mysql.connector.connect(user='root', password='password',
                                  host='127.0.0.1',
                                  database='PROJECT',
                                  auth_plugin='mysql_native_password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to database: ", record)

        print('Query 1: Find event name, event type, event date which is coming in the upcoming days \n')
        sql_select_Query = "select name, type, date from events where date >= curdate() order by date asc;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            print(row)

        print('\n\nQuery 2: Find the performer id and performer name of the top three highest salary paid to a performer ')
        sql_select_Query = "select pid,name, salary from performer p1 where 3>(select count(distinct pid) from performer p2 where p1.salary<p2.salary) order by salary desc;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            print(row)

        print('\n\nQuery 3: Find the event id, name of the events happening in Richards Hall ')
        sql_select_Query = "select e.evid,e.name from events e where e.vid=(select vid from venue where name='Richards hall');"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            print(row)

        sql_select_Query = "select department, count(eid) from employee group by department order by count(eid);"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        department = []
        count = []
        for row in records:
            department.append(row[0])
            count.append(row[1])

        plt.pie(count, labels = department)
        plt.xlabel("Department ID")
        plt.ylabel("Count of Employees")
        plt.title("Employee Info")
        plt.show()
        print('next')
        sql_select_Query = 'select pid,salary from performer;'
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        pid = []
        salary = []
        for row in records:
            pid.append(row[0])
            salary.append(row[1])

        plt.bar(pid,salary)
        plt.xlabel("Performer ID")
        plt.ylabel("Salary")
        plt.title("Performer Info")
        plt.show()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

