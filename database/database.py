from peewee import IntegerField, SqliteDatabase, CharField, Model


db = SqliteDatabase('weather.db')


class Weather(Model):
    """
    Класс создания полей в базе данных для
    хранения информации о запросах пользователя
    """
    user_id = IntegerField()
    name = CharField()
    request = CharField()
    date = CharField()

    class Meta:
        database = db
