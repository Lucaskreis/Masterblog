from flask import Flask, render_template, jsonify, request, redirect
import json
app = Flask(__name__)


# Function to load posts from Json file
def load_posts():
    with open("static/data.json") as file_obj:
        blog_posts = json.load(file_obj)
        return blog_posts


# Function to save posts to JSON file
def save_posts(posts):
    with open("static/data.json", 'w') as file_obj:
        json.dump(posts, file_obj, indent=4)


# Route to display all blog posts
@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


# Route to display add post form and handle form submission
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        posts = load_posts()
        post_id = len(posts) + 1
        new_post = {
            'id': post_id,
            'author': author,
            'title': title,
            'content': content
        }
        posts.append(new_post)
        save_posts(posts)
    return render_template('add.html')


# Route to delete a blog post
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            save_posts(posts)
            return redirect('/')
    return jsonify({'message': 'Post not found'})


# Route to display the update form and update the blog post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            if request.method == 'GET':
                return render_template('update.html', post=post, post_id=post_id)
            elif request.method == 'POST':
                post['author'] = request.form['author']
                post['title'] = request.form['title']
                post['content'] = request.form['content']
                save_posts(posts)
                return redirect('/')
    return jsonify({'message': 'Post not found'})


if __name__ == '__main__':
    app.run(debug=True)
