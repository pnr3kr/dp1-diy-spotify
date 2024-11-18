import os
import mysql.connector
from mysql.connector import Error

# Database connection details
DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "pnr3kr"

try:
    db = mysql.connector.connect(
        host=DBHOST,
        user=DBUSER,
        password=DBPASS,
        database=DB
    )
    cur = db.cursor()
    print("Connected to the database!")
except Error as e:
    print(f"Error connecting to database: {e}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}

@app.get('/songs')
def get_songs():
    query = """
        SELECT songs.title, songs.album, songs.artist, songs.year, 
               songs.file, songs.image, genres.genre
        FROM songs
        JOIN genres ON songs.genre = genres.genreid
        ORDER BY songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = [dict(zip(headers, row)) for row in results]
        return json_data
    except Error as e:
        return {"Error": f"MySQL Error: {e}"}


