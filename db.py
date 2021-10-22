import re
import config as conf
import psycopg2
import datetime

def connect():
    conn = None
    if (not conn) :
        conn = psycopg2.connect(
            host=conf.PG_HOST,
            database=conf.PG_DB,
            user=conf.PG_USER,
            password=conf.PG_PASS,
            port = conf.PG_PORT)

        cursor = conn.cursor()

    print('PostgreSQL database version:')
    return conn,cursor

def get_bank(cursor):
    query = "SELECT value from bank where id = 1"
    cursor.execute(query)

    bank = int(cursor.fetchall()[0][0])
    return bank

def get_type_oper_id(cursor,event):
    query = f"SELECT id from type_oper where name_type = '{event}'"
    cursor.execute(query)

    type_oper_id = int(cursor.fetchall()[0][0])
    return type_oper_id

def get_user_id(cursor,telegram_user_id):
    query = f"SELECT id from users where telegram_user_id = {telegram_user_id}"
    cursor.execute(query)

    user_id = int(cursor.fetchall()[0][0])
    return user_id

def get_users(cursor):
    query = "SELECT telegram_user_id from users "
    cursor.execute(query)

    user_list = [x[0] for x in cursor.fetchall()]
    return user_list

def update_bank(cursor,bank):
    query = f"update bank set value = {int(bank)} where id = 1"
    cursor.execute(query)
    return True

def get_user_name(cursor,telegram_user_id):
    query = f"SELECT name from users where telegram_user_id = {telegram_user_id} "
    cursor.execute(query)

    user_name = str(cursor.fetchall()[0][0])
    return user_name

def save_history(cursor,event,telegram_user_id,sum,bank):

    type_oper_id = get_type_oper_id(cursor,event)
    date = datetime.date.today()
    print(date)
    user_id = get_user_id(cursor,telegram_user_id)
    query = f"insert into  history(date,type_oper_id,user_id,sum_tr,bank_ostatok) values ('{date}',{type_oper_id},{user_id},{sum},{bank})"
    cursor.execute(query)
    
    return True

    


def close_connect(conn,cursor):
    if (conn):
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

