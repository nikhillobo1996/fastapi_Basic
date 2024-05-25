from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schemas,database,models,oauth2
from ..database import get_db
from sqlalchemy import func



router=APIRouter(prefix="/vote",tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):

    post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} does not exist")
        


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id==current_user.id)

    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on this post")
        
        new_vote=models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote added successfully"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user {current_user.id} has already removed vote from this post")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Vote removed successfully"}
##########################################

@router.get("/voteCount/",response_model=schemas.PostOut)
def get_vote_count(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    results= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()

    print("RESULTS",results)

    return results