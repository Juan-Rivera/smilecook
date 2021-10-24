from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

# import Recipe model class
from models.recipe import Recipe


class RecipeListResource(Resource):
    # gets all published recipes
    def get(self):
        # get all published recipes
        recipes = Recipe.get_all_published()

        # initialize empty list to return
        data = []

        # iterate through recipe list appending any recipe that is published to data list
        for recipe in recipes:
            data.append(recipe.data())

        # return back data list with Status Code 200
        return {'data': data}, HTTPStatus.OK

    # creates new recipe
    @jwt_required()
    def post(self):
        # pull data from request
        data = request.get_json()

        # identify current user
        current_user = get_jwt_identity()

        # build out Recipe object from data
        new_recipe = Recipe(name=data['name'],
                            description=data['description'],
                            num_of_servings=data['num_of_servings'],
                            cook_time=data['cook_time'],
                            directions=data['directions'],
                            user_id=current_user)

        # save new recipe to recipe list
        new_recipe.save()

        # return new recipe with Status Code 201
        return new_recipe.data(), HTTPStatus.CREATED


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

