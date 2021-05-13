# from mongoengine import  Document, StringField, IntField, DateTimeField
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Song(db.Document):
    song_name = db.StringField(required=True, max_length=100, unique=True)
    song_duration = db.IntField(required=True,)
    upload_time = db.DateTimeField(required=True)


    def fetch(self, audioFileID):
        if audioFileID != None:
            collection = Song.objects(id=audioFileID).to_json()
            return collection
        collection = Song.objects().to_json()
        # date = date.getMonth()
        return collection
    
    
    def update_song(self, audioFileID, data):
        collection = Song.objects().get_or_404(id=audioFileID)
        collection.update(**data)
        return "updated successfully"


    def delete_song(self, audioFileID):
        collection = Song.objects().get_or_404(id=audioFileID)
        collection.delete()
        return "Deleted Successfully"


class Podcast(db.Document):
    podcast_name = db.StringField(required=True, max_length=100, unique=True)
    podcast_duration = db.IntField(required=True,)
    podcast_upload_time = db.DateTimeField(required=True)
    podcast_host = db.StringField(required=True, max_length=100)
    podcast_participants = db.ListField(db.StringField(max_length=100))


    def fetch(self, audioFileID):
        if audioFileID != None:
            collection = Podcast.objects(id=audioFileID).to_json()
            return collection
        collection = Podcast.objects().to_json()
        return collection


    def update_podcast(self, audioFileID, data):
        collection = Podcast.objects().get_or_404(id=audioFileID)
        collection.update(**data)
        print(collection.to_json())
        return "updated successfully"


    def delete_podcast(self, audioFileID):
        collection = Podcast.objects().get_or_404(id=audioFileID)
        collection.delete()
        return "Deleted Successfully"



class AudioBook(db.Document):
    audiobook_title = db.StringField(required=True, max_length=100, unique=True)
    audiobook_author_title = db.StringField(required=True, max_length=100)
    audiobook_narrator = db.StringField(required=True, max_length=100)
    audiobook_duration = db.IntField(required=True,)
    audiobook_upload_time = db.DateTimeField(required=True)


    def fetch(self,audioFileID):
        if audioFileID != None:
            collection = AudioBook.objects(id=audioFileID).to_json()
            return collection
        collection = AudioBook.objects().to_json()
        return collection


    def update_audiobook(self, audioFileID, data):
        collection = AudioBook.objects().get_or_404(id=audioFileID)
        collection.update(**data)
        return "updated successfully"


    def delete_audiobook(self, audioFileID):
        collection = AudioBook.objects().get_or_404(id=audioFileID)
        collection.delete()
        return "Deleted Successfully"



    