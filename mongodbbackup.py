from os.path import join
import pymongo
from bson.json_util import dumps

def test():
    print('test')
def backup_db():
    print('in--')
    backup_db_dir=r'D:\POC\Autobackup_database\backup'
    client = pymongo.MongoClient(host="", port=27018, username="", password="")
    database = client['db_services']
    print(database)
    collections = database.list_collection_names()

    for i, collection_name in enumerate(collections):
        col = getattr(database,collections[i])
        collection = col.find()
        jsonpath = collection_name + ".json"
        jsonpath = join(backup_db_dir, jsonpath)
        with open(jsonpath, 'wb') as jsonfile:
            jsonfile.write(dumps(collection).encode())

test()
backup_db()
