import pymongo
import datetime


def connect(dbUsr, dbPss, dbName):
    client = pymongo.MongoClient(
        f"mongodb+srv://{dbUsr}:{dbPss}@{dbName}.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.AudioUsers
    return db


# def getUserList(db):
#     posts = db.posts
#     query = {"tag": "ListUsers"}
#     listOb = posts.find_one(query)
#     return listOb["list"]


def addToDb(db, Name, AudioStr, nameUser=""):
    post = {
        "Name": Name,
        "Audio": AudioStr,
        "nameUser": nameUser,
        "date": datetime.datetime.now(),
    }
    posts = db.posts
    posts.insert_one(post).inserted_id


def getAll(db):
    cursor = db['posts'].find({})
    for document in cursor:
        try:
            user = document['Name']
            AudioStr = document['Audio']
            convertStringToAudio(AudioStr, "Audio/Users/", user)
        except Exception as e:
            print(f"\tNot an audio document. Tag: {document['tag']}. [{e}]")


def deleteFromDb(db, Name):
    posts = db.posts
    query = {"Name": Name}
    if (posts.find_one(query) is not None):
        print("\tDeleting post:", query["Name"])
        posts.delete_one(query)
        return 0
    else:
        print("\t\tNo need to delete post:", query["Name"])
        return 1


def getAudioFromDb(db, Name):
    posts = db.posts
    query = {"Name": Name}
    user = posts.find_one(query)
    if (user is not None):
        print("\t\tDownloading audio:", query["Name"])
        return user["Audio"]
    else:
        # print("No such user:", query["Name"])
        pass
    return -1


def convertAudioToString(AudioName):
    f = open(AudioName, 'rb')
    s = f.read()
    f.close()
    return s


def convertStringToAudio(string, path, name):
    print('\t\tConverting', name, 'audio from string to mp3.')
    f = open(f'{path}{name}', 'wb')
    f.write(string)
    f.close()
    return 0


def addUser(db, discordName):
    deleteFromDb(db, discordName)
    try:
        audioStr = convertAudioToString(f"Audio/Users/{discordName}")
    except Exception as e:
        print(f"\tInvalid name: {discordName}. [{e}]")

    addToDb(db, discordName, audioStr)
