from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('songs', user='postgres', password='12345', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Songs(BaseModel):
    title = CharField()
    artist = CharField()
    key = CharField()
    tempo = IntegerField()

db.connect()
db.drop_tables([Songs])
db.create_tables([Songs])

Songs(title='Crazy In Love', artist='Beyoncé', key='D-', tempo=100).save()
Songs(title='Watermelon Sugar', artist='Harry Styles', key='C', tempo=95).save()
Songs(title='How Deep Is Your Love', artist='Bee Gees', key='Eb', tempo=105).save()

@app.route('/songs/', methods=['GET', 'POST'])
@app.route('/songs/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Songs.get(Songs.id == id)))
        else:
            songs_list = []
            for song in Songs.select():
                songs_list.append(model_to_dict(song))
            return jsonify(songs_list)

    if request.method == 'PUT':
        body = request.get_json()
        Songs.update(body).where(Songs.id == id).execute()
        return "Song " + str(song.title) + " has been updated."

    if request.method == 'POST':
        new_song = dict_to_model(Songs, request.get_json())
        new_song.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Songs.delete().where(Songs.id == id).execute()
        return "Song " + str(song.title) + " deleted."