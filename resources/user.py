from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from utils import hash_password

from models.recipe import Recipe
from models.user import User

from schemas.recipe import RecipeSchema
from schemas.user import UserSchema

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))

recipe_list_schema = RecipeSchema(many=True)


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        if User.get_by_username(username):
            return {'message': 'username already in use'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'email already in use'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        user = User(**data)
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)

        return data, HTTPStatus.OK


class UserRecipeListResource(Resource):
    def get(self, username, visibility):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)

        return recipe_list_schema.dump(recipes), HTTPStatus.OK


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user), HTTPStatus.OK
