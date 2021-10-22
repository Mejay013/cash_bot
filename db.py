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
    query = f"SELECT id from type_oper where name_type = {event}"
    cursor.execute(query)

    type_oper_id = int(cursor.fetchall()[0][0])
    return type_oper_id

def get_user_id(cursor,telegram_user_id):
    query = f"SELECT id from users where telegram_user_id = {telegram_user_id}"
    cursor.execute(query)

    user_id = int(cursor.fetchall()[0][0])
    return user_id

def save_history(cursor,event,telegram_user_id,bank):

    type_oper_id = get_type_oper_id(cursor,event)
    date = datetime.date.today()
    user_id = get_user_id(cursor,telegram_user_id)
    query = f"insert into table history(date,type_oper_id,user_id,bank_ostatok) values ({date},{type_oper_id},{user_id},{bank})"
    try:
        cursor.execute(query)
        return True
    except:
        return False

    


def close_connect(conn,cursor):
    if (conn):
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

