from .. import models,schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter

from sqlalchemy.orm import Session

from ..database import engine,get_db
from sqlalchemy import func
from typing import List,Optional

router=APIRouter(prefix="/posts",tags=['Posts'])




##get all posts
@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):

    #     cursor.execute(""" Select * from posts """)
    #     posts =cursor.fetchall()

    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()




    return posts


##  get post based on user id
@router.get("/userID/{id}",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    #     cursor.execute(""" Select * from posts """)
    #     posts =cursor.fetchall()


    posts = db.query(models.Post).filter(models.Postb.owner_id==current_user.id).all()
    return posts


## Add post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    print(current_user)
    print(current_user.id)
    new_post=models.Post(owner_id = current_user.id, **post.dict())

    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post





##  get post based on post id
@router.get("/{id}",response_model=schemas.Post)
def get_posts(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" Select * from posts WHERE id = %s""",(str(id)))
    # post =cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # post= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id)
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")


    
    # response.status_code=status.HTTP_404_NOT_FOUND
    # return {"post not found"}
    return post



            
##  delete post based on post id
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE from posts WHERE id = %s RETURNING *""",(str(id)))
    # post =cursor.fetchone()
    # conn.commit()
    # print(post)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorised!! ")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



##  update post based on post id
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id))))

    # post =cursor.fetchone()
    # conn.commit()
    # print(post)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    # print(post)
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorised!! ")


    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

################################


