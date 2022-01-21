from flask import Flask
from flask import request
import pymongo
import os
import datetime


app = Flask(__name__)

row_count = 10

# connect database
conn_str = "mongodb+srv://eretix5:guy123@cluster0.ltm2k.mongodb.net/test"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
news_coll = client.news_bd.news_collection


@app.route('/')
def index():
    documents = news_coll.find().sort("date", pymongo.DESCENDING)

    table = '''
        <table border="2" style="width: 100%">
            <tr>
                <th>Title</th>
                <th>Type</th>
                <th>Date</th>
                <th>url</th>
                <th>Image</th>
                <th>Text</th>             
            </tr>'''
            
    for i in range(row_count):
        title = '<td>' + documents[i]['title'] + '</td>'
        type = '<td>' + documents[i]['type'] + '</td>'
        date = '<td>' + documents[i]['date'] + '</td>'
        url = '<td>' + documents[i]['url'] + '</td>'
        image = '<td><img src="' + documents[i]['img'] + '" width=250px></td>'
        text = '<td>' + documents[i]['text'] + '</td>'
      
        table += '<tr>' + title + type + date + url  + image + text + '</tr>'
    table += '</table>'
    html = '''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Article analysis</title>
            </head>
            <body>
                <h1 align="center"><a href="https://vpravda.ru">Волгоградская правда</a></h1>
                %s
            </body>
        </html>''' % table
    return html

if __name__ == "__main__":
    app.run()
