from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world'

@app.route('/about') # маршрут
def about(): # функция действия в коце маршрута
    return f'This is about page' #то что будет на странице, когда перейдем по маршруту

@app.route('/user/<username>')

def show_user_profile(username):
    return f' User {username}'

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
if __name__ == '__main__':
    app.run(debug=True)





