#!/usr/bin/python3

#import mysql python module
import mysql.connector as mysql

# function to connect to database and return handle
# this function uses the global keyword to make the
# database object and cursor global. 
def mysql_connect(host, user, password):
  global mydb
  global mycursor
  mydb = mysql.connect(
      host=host,
      user=user,
      password=password
  )
  mycursor = mydb.cursor()

#function to execute a mysql query
def mysql_query(query):
  mycursor.execute(query)

#function to create a mysql database
def mysql_createdb(name):
   print("Database to be created is: ", name)
   query = "create database " + name
   print("Query is:", query)
   mysql_query(query)

#function to list the available databases
def mysql_showdb():
   query = "show databases;"
   print("Query is:", query)
   mysql_query(query)
   for x in mycursor:
       print(x)

#test code to test the above functions
mysql_connect("localhost", "root", "Vagrant123")
print (mydb)
mysql_createdb("test12345")
mysql_showdb()
