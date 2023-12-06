import mysql.connector
from mysql.connector import errorcode
from config_params import azure_config

class MySQLConnector:
    def __init__(self, config = None):
        if config is None:
            self.config_dict = azure_config
        else:
            self.config_dict = config
        
        self.connection = None
        self.cursor = None
    
    def connect_to_db(self):
        # Construct connection string

        try:
            self.connection = mysql.connector.connect(**self.config_dict)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.connection.cursor()
        
        return True
    
    def get_cursor(self):
        return self.cursor

    def get_connection(self):
        return self.connection
    
    def close_connection(self):
        # Cleanup
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

