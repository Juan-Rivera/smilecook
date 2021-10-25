from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.recipe import RecipeSchema, RecipePaginationSchema

from models.recipe import Recipe
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipe_pagination_schema = RecipePaginationSchema(many=True)


class RecipeListResource(Resource):
    @use_kwargs({'page': fields.Int(missing=1),
                 'per_page': fields.Int(missing=20)})
    # gets all published recipes
    def get(self, page, per_page):
        # get all published recipes
        paginated_recipes = Recipe.get_all_published(page, per_page)

        # return back data list with Status Code 200
        return recipe_pagination_schema.dump(paginated_recipes), HTTPStatus.OK

    # creates new recipe
    @jwt_required()
    def post(self):
        # pull data from request
        json_data = request.get_json()

        # identify current user
        current_user = get_jwt_identity()

        data, errors = recipe_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        recipe = Recipe(**data)
        recipe.user_id = current_user
        recipe.save()

        # return new recipe with Status Code 201
        return recipe_schema.dump(recipe), HTTPStatus.CREATED


    # patches recipe
    @jwt_required()
    def patch(self, recipe_id):
        json_data = request.get_json()

        data, errors = recipe_schema.load(data=json_data, partial=('name', ))

        if errors:
            return {'message': 'Validation Errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.name = data.get('name') or recipe.name
        recipe.description = data.get('description') or recipe.description
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.directions = data.get('directions') or recipe.directions

        recipe.save()
        return recipe_schema.dump(recipe), HTTPStatus.OK


class RecipeResource(Resource):
    # gets a specific recipe
    @jwt_required()
    def get(self, recipe_id):
        # find specific recipe in recipe list
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if recipe.is_publish is False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        # return recipe with Status Code 200
        return recipe.data(), HTTPStatus.OK

    # updates recipe with new information
    @jwt_required()
    def put(self, recipe_id):
        # pull data from request
        data = request.get_json()

        # find specific recipe to update with recipe_id
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        # inject info from the data you pulled from request into recipe
        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        recipe.save()
        # return updated recipe with Status Code 200
        return recipe.data(), HTTPStatus.OK

    # deletes recipe
    @jwt_required()
    def delete(self, recipe_id):
        # find specific recipe to update with recipe_id
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        # remove recipe from recipe list
        recipe.delete()

        # return success message with Status Code 200
        return {'message': 'recipe successfully deleted'}, HTTPStatus.OK


class RecipePublishResource(Resource):
    # publishes recipe
    @jwt_required()
    def put(self, recipe_id):
        # find specific recipe in recipe list
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        # change is_publish to True (publish)
        recipe.is_publish = True

        # return nothing back
        return {}, HTTPStatus.NO_CONTENT

    # unpublishes recipe
    @jwt_required()
    def delete(self, recipe_id):
        # find specific recipe in recipe list
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        # change is_publish to False (unpublish)
        recipe.is_publish = False

        # return nothing back
        return {}, HTTPStatus.NO_CONTENT

