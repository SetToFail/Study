from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def mission_home():
    return render_template('base.html', title='Заготовка')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')