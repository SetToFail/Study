from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def mission_title():
    return "Миссия Колонизация Марса"

@app.route('/index')
def mission_motto():
    return "И на Марсе будут яблони цвести!"

@app.route('/promotion_image') 
def promotion():
    return render_template('promotion.html')

@app.route('/astronaut_selection') 
def selection():
    return render_template('selection.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')