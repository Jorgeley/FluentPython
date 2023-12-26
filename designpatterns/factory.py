import mysql.connector
import psycopg2 as postgres
from abc import ABC
from enum import Enum

"""
A Factory class, as the name suggests, it's simply an abstract class which
holds the logic for fabricating objects
"""


class DBDriver(Enum):
    # Database constants
    POSTGRES = 1
    MYSQL = 2
    # more constants...


class Factory(ABC):
    # Final Class - Factory to return connect object
    __postgresConn = None
    __mysqlConn = None
    # more connections vars...

    @classmethod
    def connect(cls, dao):
        """
        Returns a connection
        
        Arguments:
            dao {Enum} -- Database driver constant
        
        Returns:
            any -- connection with a datasource
        """
        if dao == DBDriver.POSTGRES:
            if not cls.__postgresConn:
                print('pg')
                cls.__postgresConn = postgres.connect(
                    "host=localhost port=5432 dbname=mydb user=myuser"
                )
            return cls.__postgresConn
        elif dao == DBDriver.MYSQL:
            if not cls.__mysqlConn:
                print('mysql')
                cls.__mysqlConn = mysql.connector.connect(
                    user='myuser',
                    password='password',
                    host='localhost',
                    database='mydb'
                )
            return cls.__mysqlConn
        else: raise NotImplementedError("DB Driver not implemented")


# Usage:
pg_conn = Factory.connect(DBDriver.POSTGRES)
mysql_conn = Factory.connect(DBDriver.MYSQL)