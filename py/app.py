from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import cross_origin, CORS
from bson import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myData'
mongo = PyMongo(app)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})


@app.route('/posts', methods=['GET'])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def get_posts():
    all_posts = []
    for post in mongo.db.posts.find():
        str_comments = []
        for comment in post['comments']:
            comment_object = {
                'id': str(comment['_id']),
                'content': comment['content']
            }
            str_comments.append(comment_object)
        post_object = {
            'id': str(post['_id']),
            'title': post['title'],
            'content': post['content'],
            'status': post['status'],
            'comments': str_comments
        }
        all_posts.append(post_object)
    return (all_posts)


@app.route('/posts/newPost', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def new_post():
    post_title = request.get_json(force=True)['title']
    post_content = request.get_json(force=True)['content']
    post_status = request.get_json(force=True)['status']
    post_comments = request.get_json(force=True)['comments']
    mongo.db.posts.insert_one({"title": post_title, "content": post_content,
                               "status": post_status, "comments": post_comments})
    return 'h'


@app.route('/posts/editlike/<string:id>', methods=['GET', 'PUT'])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def like(id):
    post = mongo.db.posts.find_one({"_id": ObjectId(id)})
    mongo.db.posts.update_one({"_id": ObjectId(id)}, {
                              "$set": {"status": not post["status"]}})
    return "h"


@app.route('/posts/delete/<string:id>', methods=["DELETE"])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def delete_post(id):
    mongo.db.posts.delete_one({"_id": ObjectId(id)})
    return 'h'


@app.route('/posts/editPost', methods=['GET', 'PUT'])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def edit_post():
    post_id = request.get_json(force=True)['id']
    post_title = request.get_json(force=True)['title']
    post_content = request.get_json(force=True)['content']
    mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {
                              "$set": {"title": post_title, "content": post_content}})
    return 'h'


@app.route('/posts/newcomment', methods=['GET', 'PUT'])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def new_comment():
    post_id = request.get_json(force=True)['post_id']
    n_comment = request.get_json(force=True)['content']
    comment_object = {
        '_id': ObjectId(),
        'content': n_comment
    }
    mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {
                              "$push": {"comments": comment_object}})
    return "h"


@app.route('/posts/deleteComment', methods=['GET', 'PUT'])
@cross_origin(origin='localhost', headers=["content-type", "Authorization", "Access-Control-Allow-Origin"])
def delete_comment():
    post_id = request.get_json(force=True)['post_id']
    comment_id = request.get_json(force=True)['comment_id']
    mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {
                              "$pull": {"comments": {"_id": ObjectId(comment_id)}}})
    return 'h'


if __name__ == "__main__":
    app.run(debug=True)
