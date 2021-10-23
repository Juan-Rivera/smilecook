from flask import Flask
from flask_restful import Api

# import resource classes
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource

# initialize app, and api here (Api basically does some behind the scenes stuff for us so we don't have to :) )
app = Flask(__name__)
api = Api(app)

# adding endpoints here, match endpoints with the specific resource class you want it to hit
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

if __name__ == '__main__':
    # running app, setting port to localhost:5000, debug true
    app.run(port=5000, debug=True)