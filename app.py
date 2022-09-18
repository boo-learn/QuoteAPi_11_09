from api import api, app
from api.resources.quote import QuoteResource, QuoteListResource
from api.resources.author import AuthorResource
from api.resources.user import UserResource, UsersListResource
from config import Config

api.add_resource(QuoteListResource,
                 '/authors/<int:author_id>/quotes', # GET POST
                 '/quotes'  # GET
                 )
api.add_resource(QuoteResource,
                 '/authors/<int:author_id>/quotes/<int:quote_id>', # GET PUT DELETE
                 )
api.add_resource(AuthorResource,
                 '/authors/<int:author_id>',
                 '/authors')  # <-- requests
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # <-- requests
api.add_resource(UsersListResource,
                 '/users')  # <-- requests

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
