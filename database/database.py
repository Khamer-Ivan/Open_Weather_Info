from peewee import *

db = SqliteDatabase('weather.db')


class Weather(Model):
    user_id = IntegerField()
    name = CharField()
    request = CharField()
    date = CharField()

    class Meta:
        database = db
