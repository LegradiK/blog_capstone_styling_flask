from flask import Flask, render_template
import requests

app = Flask(__name__)

response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
response.raise_for_status()
blog_articles = response.json()

@app.route('/')
def home():
    return render_template("index.html", blog=blog_articles)

@app.route('/posts/<int:id>')
def posts(id):
    return render_template("post.html", blog=blog_articles, id=id)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)