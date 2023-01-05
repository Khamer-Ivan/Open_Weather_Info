from peewee import *

db = SqliteDatabase('weather.db')


class Weather(Model):
    user_id = IntegerField()
    name = CharField()
    request = CharField()
    date = DateField()

    class Meta:
        database = db


Weather.create_table()

# with sq.connect('weather.db') as con:
#     cur = con.cursor()
#
#     # cur.execute('DROP TABLE IF EXISTS weather')
#     cur.execute(
#         """
#                 CREATE TABLE IF NOT EXISTS weather
#                 (
#                 id INTEGER,
#                 name TEXT,
#                 request TEXT,
#                 date DATETIME
#                 )
#                 """
#                 )

