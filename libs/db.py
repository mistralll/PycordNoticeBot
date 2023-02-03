import sys
sys.path.append('../')

import psycopg2
import libs.env as env

def new_db_connection():
    connection = psycopg2.connect(host=env.HOST, user=env.USER, password=env.PASS, database=env.NAME, port=env.PORT)
    return connection

def add_notice_channel_id(voice_ch_id, text_ch_id):
    connection = new_db_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO notice_channel (voice_ch_id, text_ch_id) VALUES (%s, %s)"
            cursor.execute(sql, (voice_ch_id, text_ch_id))
        connection.commit()

def get_all_notice_channel_ids():
    connection = new_db_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT voice_ch_id, text_ch_id FROM notice_channel"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

def get_notice_channel_id(voice_ch_id):
    connection = new_db_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT voice_ch_id, text_ch_id FROM notice_channel WHERE voice_ch_id = %s"
            cursor.execute(sql, [voice_ch_id])
            result = cursor.fetchall()
            return result

def update_db(voice_ch_id, text_ch_id):
    connection = new_db_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE notice_channel SET text_ch_id = %s WHERE voice_ch_id = %s"
            cursor.execute(sql, (text_ch_id, voice_ch_id))
            connection.commit()

def delete_db_row(voice_ch_id):
    connection = new_db_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM notice_channel WHERE voice_ch_id = %s"
            cursor.execute(sql, [voice_ch_id])
            connection.commit()

def delete_all_db_rows():
    connection = new_db_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM notice_channel"
            cursor.execute(sql)
            connection.commit()

def change_or_add_notice_channel(voice_ch_id, text_ch_id):
    prev = get_notice_channel_id(voice_ch_id)
    if not prev:
        add_notice_channel_id(voice_ch_id, text_ch_id)
    else:
        update_db(voice_ch_id, text_ch_id)

