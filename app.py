import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Helper function to fetch blog post by ID
def fetch_post_by_id(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    # Read the blog posts data from the JSON file
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Read the blog posts data from the JSON file
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)

        # Get data from the form and add a new blog post
        new_post = {
            'id': len(blog_posts) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        blog_posts.append(new_post)

        # Write the updated 'blog_posts' list to the JSON file with indentation
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post details based on the data from the form
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Read the blog posts data from the JSON file
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)

        # Update the blog_posts list in memory (if needed)
        for blog_post in blog_posts:
            if blog_post['id'] == post_id:
                blog_post['author'] = post['author']
                blog_post['title'] = post['title']
                blog_post['content'] = post['content']
                break

        # Write the updated 'blog_posts' list to the JSON file with indentation
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # Read the blog posts data from the JSON file
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    # Find the index of the blog post with the given post_id
    index_to_delete = None
    for index, post in enumerate(blog_posts):
        if post['id'] == post_id:
            index_to_delete = index
            break

    # If the blog post with the post_id is found, remove it from the list
    if index_to_delete is not None:
        del blog_posts[index_to_delete]

        # Write the updated 'blog_posts' list to the JSON file with indentation
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

    # Redirect the user back to the home page after successful deletion
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
