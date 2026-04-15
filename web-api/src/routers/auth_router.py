from fastapi import APIRouter, Response

from src.data_access.data_access import SessionLocal
from src.models.user_model import LoginModel
from src.data_models.user_data_model import UserDataModel
from src.models.auth_user_model import AuthUserModel
from src.utils.auth_helper import (
    create_access_token,
    get_password_hash,
    verify_passwords,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("")
async def get_auth(login: LoginModel):

    with SessionLocal() as session:
        user = (
            session.query(UserDataModel)
            .where(UserDataModel.email == login.email)
            .first()
        )
        if user is None:
            return Response(status_code=403)

        hashed_password = get_password_hash(login.password)

        if verify_passwords(hashed_password, user.password):
            return Response(status_code=401)

        access_token = create_access_token(data={"sub": user.email}, expires_delta=None)

    return AuthUserModel(user_id=user.id, token=access_token)
