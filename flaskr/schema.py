from marshmallow import fields

from flaskr import ma


class ReplySchema(ma.Schema):
    id = fields.Integer()
    content = fields.String()


class CommentSchema(ma.Schema):
    id = fields.Integer()
    content = fields.String()
    replies = fields.List(fields.Nested(ReplySchema))


class PostSchema(ma.Schema):
    id = fields.Integer()
    content = fields.String()
    up_vote = fields.List(fields.Integer())
    down_vote = fields.List(fields.Integer())
    comments = fields.List(fields.Nested(CommentSchema))



post_schema = PostSchema()
post_schemas = PostSchema(many=True)

comment_schema = CommentSchema()
comment_schemas = CommentSchema(many=True)

reply_schema = ReplySchema()
reply_schemas = ReplySchema(many=True)
