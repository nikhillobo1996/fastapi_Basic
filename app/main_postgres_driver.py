# from fastapi import FastAPI,Response,status,HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content:str
#     published: bool = True
#     rating: Optional[int] = None

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database = 'fastapi',user='postgres',password='Qwerty1234$',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connected successfully")
#         break

#     except Exception as error:
#         print(f"error:{error}")
#         time.sleep(2)


# my_posts = [{"title":"title1","content":"content1","id":1},{"title":"title2","content":"content2","id":2}]


# @app.get("/")
# async def root():
#     return {"message": "How you doin?"}

# @app.get("/posts")
# def get_posts():
#     cursor.execute(""" Select * from posts """)
#     posts =cursor.fetchall()
#     return {'data':posts}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post ):
#     cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))

#     new_post=cursor.fetchone()
#     conn.commit()

#     return {'data':new_post}

# @app.get("/posts/{id}")
# def get_posts(id:int,response:Response):
#     cursor.execute(""" Select * from posts WHERE id = %s""",(str(id)))
#     post =cursor.fetchone()
    

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
#     # response.status_code=status.HTTP_404_NOT_FOUND
#     # return {"post not found"}
#     return {"post_detail":post}

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cursor.execute(""" DELETE from posts WHERE id = %s RETURNING *""",(str(id)))
#     post =cursor.fetchone()
#     conn.commit()
#     print(post)


#     if post ==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     cursor.execute(""" UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id))))

#     post =cursor.fetchone()
#     conn.commit()
#     print(post)

#     if post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")


#     return {"data":post}
