from flask import Flask, render_template
import json

app = Flask(__name__)

with open("storage/posts.json", "r") as posts_file:
    blog_posts = json.load(posts_file)

@app.route('/')
def index():
    #code comes here
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)