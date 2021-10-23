from flask import request
from flask_restful import Resource
from http import HTTPStatus

# import Recipe class and recipe list
from models.recipe import Recipe, recipe_list


class RecipeListResource(Resource):
    # gets all published recipes
    def get(self):
        # initialize empty list to return
        data = []

        # iterate through recipe list appending any recipe that is published to data list
        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)

        # return back data list with Status Code 200
        return {'data': data}, HTTPStatus.OK

    # creates new recipe
    def post(self):
        # pull data from request
        data = request.get_json()

        # build out Recipe object from data
        new_recipe = Recipe(name=data['name'],
                            description=data['description'],
                            number_of_servings=data['number_of_servings'],
                            cook_time=data['cook_time'],
                            directions=data['directions'])

        # append new recipe to recipe list
        recipe_list.append(new_recipe)

        # return new recipe with Status Code 201
        return new_recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):
    # gets a specific recipe
    def get(self, recipe_id):
        # find specific recipe in recipe list
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish is True), None)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # return recipe with Status Code 200
        return recipe.data, HTTPStatus.OK

    # updates recipe with new information
    def put(self, recipe_id):
        # pull data from request
        data = request.get_json()

        # find specific recipe to update with recipe_id
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # inject info from the data you pulled from request into recipe
        recipe.name = data['name']
        recipe.description = data['description']
        recipe.number_of_servings = data['number_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        # return updated recipe with Status Code 200
        return recipe.data, HTTPStatus.OK

    # deletes recipe
    def delete(self, recipe_id):
        # find specific recipe to update with recipe_id
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # remove recipe from recipe list
        recipe_list.remove(recipe)

        # return success message with Status Code 200
        return {'message': 'recipe successfully deleted'}, HTTPStatus.OK


class RecipePublishResource(Resource):
    # publishes recipe
    def put(self, recipe_id):
        # find specific recipe in recipe list
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # change is_publish to True (publish)
        recipe.is_publish = True

        # return nothing back
        return {}, HTTPStatus.NO_CONTENT

    # unpublishes recipe
    def delete(self, recipe_id):
        # find specific recipe in recipe list
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        # if no recipe found, return error message with Status Code 404
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        # change is_publish to False (unpublish)
        recipe.is_publish = False

        # return nothing back
        return {}, HTTPStatus.NO_CONTENT

