from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index/<title>')
def index(title='Заготовка'):
    return render_template('base.html', title=title)

@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)

@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = [
        "Инженер-исследователь",
        "Пилот",
        "Строитель",
        "Экзобиолог",
        "Врач",
        "Инженер по терраформированию",
        "Климатолог",
        "Специалист по радиационной защите",
        "Астрогеолог",
        "Гляциолог",
        "Инженер жизнеобеспечения",
        "Метеоролог",
        "Оператор марсохода",
        "Киберинженер",
        "Штурман",
        "Пилот Дронов"
    ]
    return render_template('list_prof.html', list_type=list_type, professions=professions)

@app.route('/answer')
@app.route('/auto_answer')
def answer():
    data = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'высшее',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': 'True'
    }
    return render_template('auto_answer.html', **data)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')