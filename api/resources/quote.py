from api import Resource, reqparse, db, auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema, quotes_schema
from flask import g


class QuoteListResource(Resource):
    def get(self, author_id=None):
        if author_id is None:  # Если запрос приходит по url: /quotes
            quotes = QuoteModel.query.all()
            return quotes_schema.dump(quotes), 200  # Возвращаем ВСЕ цитаты

        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404
        quotes = author.quotes.all()
        return quotes_schema.dump(quotes), 200  # Возвращаем все цитаты автора

    @auth.login_required
    def post(self, author_id):
        print(g.user.username)
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        quote_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quote = QuoteModel(author, quote_data["text"])
        db.session.add(quote)
        db.session.commit()
        return quote_schema.dump(quote), 201


class QuoteResource(Resource):
    def get(self, author_id=None, quote_id=None):
        """
        Обрабатываем GET запросы
        :param author_id: id автора
        :param quote_id: id цитаты
        :return: http-response(json, статус)
        """
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": "Author not found"}, 404

        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return {"Error": "Quote not found"}, 404

        if quote.author.id != author.id:
            return {"Error": "Цитата не принадлежит автору"}, 400
        return quote_schema.dump(quote), 200


    # PUT: /authors/1/quotes/1
    # PUT: /authors/2/quotes/1  <-- 400 "Цитата не принадлежит автору"
    # PUT: /authors/10/quotes/1
    def put(self, author_id, quote_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        new_data = parser.parse_args()

        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return {"Error": "Quote not found"}, 404

        if quote.author.id != author.id:
            return {"Error": "Цитата не принадлежит автору"}, 400
        quote.text = new_data["text"]
        db.session.commit()
        return quote.to_dict(), 200

    def delete(self, author_id, quote_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404
        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return {"Error": f"Quote id={quote_id} not found"}, 404
        if quote.author.id != author.id:
            return {"Error": "Цитата не принадлежит автору"}, 400
        db.session.delete(quote)
        db.session.commit()
        return "", 204
