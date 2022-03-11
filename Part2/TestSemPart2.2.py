from pymongo import MongoClient
import re

client = MongoClient("mongodb+srv://eretix5:guy123@cluster0.ltm2k.mongodb.net/test")
db = client.get_database('news_bd')
collection = db.sentence

db_documents = list(collection.find({}))
db_documenta = list(collection.find({}))
with open('запас.txt', 'w', encoding="utf-8") as f:
    for i in range(len(list(db_documents))):
        f.write('\n')
        f.write('Статья номер ')
        f.write(re.sub(r'\', \'', ' ', str(db_documents[i]['_id'])))
        f.write('\n')
        f.write(re.sub(r'\', \'', ' ', str(db_documenta[i]['sentence'])))
        f.write('\n\n')
    f.close()