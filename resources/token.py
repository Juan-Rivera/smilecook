from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from http import HTTPStatus

from utils import check_password
from models.user import User


block_list = set()


class TokenResource(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': access_token}, HTTPStatus.OK


class RevokeResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        block_list.add(jti)

        return {'message': 'Successfully logged out'}, HTTPStatus.OK
