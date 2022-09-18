from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.schemas.author import AuthorSchema, authors_schema, author_schema


class AuthorResource(Resource):
    #          ma       flask
    # Object ----> dict ----> JSON
    def get(self, author_id=None):  # Если запрос приходит по url: /authors
        if author_id is None:
            authors = AuthorModel.query.all()
            # return AuthorSchema(many=True).dump(authors)
            return authors_schema.dump(authors)
            # authors_list = [author.to_dict() for author in authors]
            # return authors_list, 200

        # Если запрос приходит по url: /authors/<int:author_id>
        author = AuthorModel.query.get(author_id)
        if author is None:
            return f"Author id={author_id} not found", 404

        return author_schema.dump(author), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("surname", required=True)
        author_data = parser.parse_args()
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
        return author_schema.dump(author), 201

    def put(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        author_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404
        author.name = author_data["name"]
        db.session.commit()
        return author.to_dict(), 200

    def delete(self, author_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404
        db.session.delete(author)
        db.session.commit()
        return "", 204
