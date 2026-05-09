from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

@router.post("/token/")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.username == request.username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    access_token = auth.create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }