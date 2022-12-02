import pymongo
import datetime
import random


def connect(dbUsr, dbPss, dbName):
    client = pymongo.MongoClient(
        f"mongodb+srv://{dbUsr}:{dbPss}@{dbName}.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.AudioList
    return db


def convertAudioToString(AudioName):
    f = open(AudioName, 'rb')
    s = f.read()
    f.close()
    return s


def convertStringToAudio(string, path, name):
    print(f'\tConverting {name} audio from string to mp3.')
    f = open(str(path) + str(name), 'wb')
    f.write(string)
    f.close()
    return 0


def getRandomAudio(db):
    N = db.posts.count_documents({})
    R = random.randint(0, N - 1)
    randomEle = db.posts.find(
        {}, {"Name": 1, "Creator": 1, 'date': 1}
    ).limit(1).skip(R)
    randomEle = randomEle[0]
    if (randomEle is not None):
        print(f"\tRandomizing audio: {randomEle['Name']}")
        return (randomEle['Name'])
    else:
        print(f"\tError in element: {randomEle}")
    return -1


def getAudioFromDb(db, Name):
    posts = db.posts
    query = {"Name": Name}
    user = posts.find_one(query)
    if (user is not None):
        print(f"\tDownloading audio: {query['Name']}")
        return user["Audio"]
    else:
        print(f"\tNo such file: {query['Name']}")
    return -1


def getAllInfo(db):
    listInfo = dict()
    cursor = db['posts'].find(
        {}, {"Name": 1, "Creator": 1, 'date': 1}
    )
    for document in cursor:
        try:
            audioName = document['Name']
            creator = document['Creator']
            creationTime = document['date']
            listInfo[audioName] = [creator, creationTime]
        except Exception as e:
            print(f'\tException on listAudioManager.getAllInfo [{e}]')

    return listInfo


def getAll(db):
    listInfo = dict()
    cursor = db['posts'].find({})
    for document in cursor:
        try:
            audioName = document['Name']
            AudioStr = document['Audio']
            creator = document['Creator']
            creationTime = document['date']
            convertStringToAudio(AudioStr, "Audio/", audioName)
            listInfo[audioName] = [creator, creationTime]
        except Exception as e:
            print(f'\tException on listAudioManager.getAll [{e}]')

    return listInfo


def addToDb(db, Name, AudioStr, author_id):
    post = {
        "Name": Name,
        "Audio": AudioStr,
        'Creator': author_id,
        "date": datetime.datetime.now()
    }
    posts = db.posts
    posts.insert_one(post).inserted_id
    return post


def deleteFromDb(db, Name):
    posts = db.posts
    query = {"Name": Name}
    if (posts.find_one(query) is not None):
        print("    Deleting post:", query["Name"])
        posts.delete_one(query)
        return 0
    else:
        print("    No such user:", query["Name"])
        return 1
