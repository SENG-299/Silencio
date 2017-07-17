from .server_stored_user import stored_user
from .server_stored_chatroom import stored_chatroom

import pymysql

class database(object):
    """Database class for the server that is designed to cold store all user and chatroom info"""
    #this will change if we run off nolans computer. will update if/when necessary
    db = ("localhost", "Avery", "test", "CHAT_DATABASE")

    def __init__(self):
        self.con = pymysql.connect(*self.db)
        self.cursor = self.con.cursor()
     
#inserts a user if the user isn't already there.
    def insert(self, user):

        if self.query("name", user.name) is None:
            self.cursor.execute("""INSERT into users VALUES (NULL, %s, %s, %s)""",(user.name,
                user.password,user.alias))
            self.con.commit()
        else:
        	print ("ID already taken")

#query finds a user given the column(id, name, or alias)and returns the user if found
    def query(self, column, value):

        if column is 'id':
            self.cursor.execute("""SELECT * from users WHERE id =(%s)""",(value))
        elif column is 'name':
            self.cursor.execute("""SELECT * from users WHERE name =(%s)""",(value))
        elif column is 'alias':
            self.cursor.execute("""SELECT * from users WHERE alias =(%s)""",(value))            
        temp = self.cursor.fetchone()
    #If a user is found, return it
        if temp is not None:
            temp_user = user(temp[1],temp[2], temp[3]) 
            return temp_user
        else:
            print ("No User matching that id")       

#retrieves an id of a given user 
    def retrieve_id(self, user):
        self.cursor.execute("""SELECT id from users WHERE name=(%s)""",(user.name))
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            print ("No id matching that id")

#returns total number of users
    def num_users(self):
        self.cursor.execute("""SELECT COUNT(*) FROM users""")
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            print ("Table is empty")
