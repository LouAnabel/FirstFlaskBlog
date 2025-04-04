from flask import Flask, request, redirect, render_template, url_for
import os
import json

app = Flask(__name__)


def read_json(file_path='storage/posts.json'):
    """load data from json file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_json(posts, file_path='storage/posts.json'):
    """write data into json file"""

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(posts, file, indent=2)


@app.route('/')
def index():
    """run index template"""
    blog_posts = read_json()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """add a post and run the add-template"""
    if request.method == 'POST':
        # Print form data for debugging
        print("Form data received:", request.form)

        # Basic validation
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            return render_template('add.html', error="Title and content are required.")

        # Retrieve json list of posts
        blog_posts = read_json()

        if blog_posts:
            new_id = max(post.get('id', 0) for post in blog_posts) + 1
        else:
            new_id = 1

        # Create the new post dictionary with the incremented ID
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        print(new_post)
        # Append the new post to the list
        blog_posts.append(new_post)

        # Write the updated posts back to the JSON file
        write_json(blog_posts)

        # After writing to JSON
        print("Added new post:", new_post)
        print("Current posts:", blog_posts)

        # Redirect or return a response
        return redirect(url_for('index'))

    return render_template('add.html')

def fetch_post_by_id(post_id):
    """search for post that is selected by the user"""
    blog_posts = read_json()
    fetched_post = None

    for post in blog_posts:
        if post['id'] == post_id:
            fetched_post = post
    return fetched_post

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """find the id of the post to delete"""
    blog_posts = read_json()
    post_to_remove = fetch_post_by_id(post_id)

    if post_to_remove:
        blog_posts.remove(post_to_remove)
        write_json(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):

    # Fetch the blog posts from the JSON file
    post_to_update = fetch_post_by_id(post_id)

    if post_to_update is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Basic validation
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            return render_template('update.html', error="Title and content are required.")

        # Create the new post dictionary with the incremented ID
        updated_post = {
            "id": post_id, #keep the existing post ID
            "author": author,
            "title": title,
            "content": content
        }

        # Retrieve json list of posts
        blog_posts = read_json()

        # Find and update the post in the list
        for i, existing_post in enumerate(blog_posts):
            if existing_post["id"] == post_id:
                blog_posts[i] = updated_post
                break

        # Update the post in the JSON file
        write_json(blog_posts)

        # Redirect back to index or to the post detail page
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post_to_update)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)



