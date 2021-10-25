import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_uploads import configure_uploads

from extensions import db, jwt, image_set

from resources.user import UserListResource, UserResource, UserRecipeListResource, UserAvatarUploadResource, MeResource
from resources.token import TokenResource, RefreshResource, RevokeResource, block_list
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource

migrate = Migrate()


# initialize app with config from files config.py
def create_app():
    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        config_str = 'config.ProductionConfig'
    elif env == 'Staging':
        config_str = 'config.StagingConfig'
    else:
        config_str = 'config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    configure_uploads(app, image_set)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token_in_blocklist = jti in block_list
        return token_in_blocklist


def register_resources(app):
    api = Api(app)

    # adding endpoints here, match endpoints with the specific resource class you want it to hit
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')
    api.add_resource(MeResource, '/me')


if __name__ == '__main__':
    app = create_app()
    app.run()
