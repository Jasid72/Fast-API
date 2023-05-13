import mysql.connector
from fastapi.openapi.models import Response
from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
import time
from App.Database import engine
from App.schemas import CreatePost
import sys
sys.path.append(r"A:\Fast-API\App")
import model


model.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="root1234",
            database="fastapi"
        )
        print("Connected")
        break
    except Exception as error:
        print("Connection Failed")
        print("Error", error)
        time.sleep(2)


@app.get("/")
def index():
    return {"My First Api"}


mycursor = mydb.cursor()


@app.get("/posts")
def index():
    query = "SELECT * FROM post"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    print(myresult)
    return {"Post": myresult}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost):

    query = "insert into post(title, content) values (%s, %s)"
    query2 = "SELECT * FROM post"
    mycursor.execute(query, (post.title, post.content))
    mycursor.execute(query2)
    myresult = mycursor.fetchall()
    mydb.commit()
    return {"data": myresult}


@app.get("/posts/{id}")
def get_post(id: str):
    query = f"select * from post where id = {id}"
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    mydb.commit()
    if not myresult:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post ID {id} was not Found.")
    return {"Here is your Post ID:": myresult}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str):

    query = f"delete from post where id = {id}"
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    mydb.commit()
    if myresult==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT, detail="Post was deleted")


@app.put("/posts/{id}")
def update(id: str, post: CreatePost):

    query = f"update post set title = %s, content = %s, published = %s where id= {id}"
    query2 = f"select * from post where id = {id}"
    values = (post.title, post.content, post.published)
    mycursor.execute(query, values)
    mycursor.execute(query2)
    myresult = mycursor.fetchone()
    mydb.commit()
    if myresult == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist ")
    return {'Data': myresult}



