from django.db import models
import dbConnectionFunctions as db
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def acceptApplicant(userEmail, reasoning, password):
    conn = db.getDB()
    cursor = db.getCursor(conn)

    args = [userEmail, reasoning, password]
    result_args = cursor.callproc('acceptApplicant', args)

    cursor.close()
    conn.close()


def rejectApplicant(userEmail, reasoning):
    conn = db.getDB()
    cursor = db.getCursor(conn)

    args = [userEmail, reasoning]
    result_args = cursor.callproc('rejectApplicant', args)

    cursor.close()
    conn.close()


# Create your models here.
