from flask import Flask,request,make_response,Response
from flask_mongoengine import MongoEngine
from model import Song,db,Podcast,AudioBook
import datetime
import json

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'audiodb',
    'host': 'localhost',
    'port': 27017
}
db.init_app(app)


@app.route("/<string:audioFileType>/", defaults={'audioFileID':None})
@app.route("/<string:audioFileType>/<audioFileID>",methods=["GET"])
def get_audio_file(audioFileType,audioFileID):
    """This route is used to retrive the corresponding documents of Song,Podcast,AudioBook"""
    try:
        audioFileType = audioFileType.capitalize()
        if audioFileType == "Song":
            val = Song()
            data = val.fetch(audioFileID)

        elif audioFileType == "Podcast":
            val = Podcast()
            data = val.fetch(audioFileID)
            # data = json.dumps(data)
            print(data)

        elif audioFileType == "Audiobook" or "AudioBook":
            val = AudioBook()
            data = val.fetch(audioFileID)

        return data
    except Exception as ex:
        return  Response("Error occured", status=500)


@app.route("/<string:audioFileType>/<audioFileID>",methods=["PUT"])
def update_record(audioFileType, audioFileID):
    """This route is used to Update the corresponding documents of Song,Podcast,AudioBook"""
    try:
        request_data = request.get_json()   
        audioFormat = audioFileType.lower()
        data = request_data['audioFileMetadata']
        if audioFormat == "song":
            response_msg = Song().update_song(audioFileID, data)
        elif audioFormat == "podcast":
            response_msg = Podcast().update_podcast(audioFileID, data)
        elif audioFormat == "audiobook":
            response_msg = AudioBook().update_audiobook(audioFileID, data)
        return Response(response_msg,status=200)
    except Exception as ex:
        return Response("Error occured", status=500)


@app.route("/create",methods = ["POST"])
def create_record():
    """This route is used to create new Songs,Podcast,Audiobook
       audioFileType(type of the file to be created
       audioFileMetadata (data to be inserted)"""
    try:
        request_data = request.get_json()   
        audioFormat = request_data['audioFileType']
        data = request_data['audioFileMetadata']
        audioFormat = audioFormat.lower()
        if audioFormat == "song":
            new_song = Song(
                song_name=data['song_name'],
                song_duration=data['song_duration'],
                upload_time=datetime.datetime.now()
            )
            new_song.save()
            resp_msg = "song inserted successfully"
        elif audioFormat == "podcast":
            if "podcast_participants" in data:
                if data['podcast_participants']<10:
                    new_podcast = Podcast(
                        podcast_name=data['podcast_name'],
                        podcast_duration=data['podcast_duration'],
                        podcast_upload_time=datetime.datetime.now(),
                        podcast_host=data['podcast_host'],
                        podcast_participants=data['podcast_participants']
                    )
                else:
                    return Response("Error Occured", status = 500)
            else:
                new_podcast = Podcast(
                        podcast_name=data['podcast_name'],
                        podcast_duration=data['podcast_duration'],
                        podcast_upload_time=datetime.datetime.now(),
                        podcast_host=data['podcast_host'],
                    )
            new_podcast.save()
            resp_msg = "podcast inserted successfully"

        elif audioFormat == "audiobook":
            new_audiobook = AudioBook(
                audiobook_title=data['audiobook_title'],
                audiobook_author_title=data['audiobook_author_title'],
                audiobook_narrator=data['audiobook_narrator'],
                audiobook_duration=data['audiobook_duration'],
                audiobook_upload_time=datetime.datetime.now()
            )
            new_audiobook.save()
            resp_msg = "audiobook inserted successfully"

        return Response(resp_msg,status=200)
    except Exception as ex:
        return Response("Error occured", status=500)
    

@app.route("/delete/<string:audioFileType>/<audioFileID>",methods = ["DELETE"])
def delete_document(audioFileType, audioFileID):
    """This route is used to delete the corresponding documents of Song,Podcast,AudioBook"""
    try:
        audioFormat = audioFileType.lower()
        if audioFormat == "song":
            resp_msg = Song().delete_song(audioFileID)
        elif audioFormat == "podcast":
            resp_msg = Podcast().delete_podcast(audioFileID)
        elif audioFormat == "audiobook":
            resp_msg = AudioBook().delete_audiobook(audioFileID)
        return Response(resp_msg,status=200)
    except Exception as ex:
        print(ex)
        return Response("Error occured", status=500)


if __name__ == '__main__' :
    app.run(debug=True,port=8080)