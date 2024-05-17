#Test Flask

from flask import Flask, render_template


# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')

#def index():
#    return "<h1>Hello World!</h1>"

#FILTERS
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags


def index():
    first_name = "Akmal"
    stuff = "This is <strong>Bold</strong> Text"
    
    favorite_pizza = ["Pepperoni", "Cheese", "Mushroom", 41]
    return render_template("index.html",
                           first_name = first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)

# localhost:5000/user/john
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)