from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Job:
    def __init__(self, id, title, team_leader, work_size, collaborators, is_finished=False):
        self.id = id
        self.title = title
        self.team_leader = team_leader
        self.work_size = work_size
        self.collaborators = collaborators
        self.is_finished = is_finished
        self.start_date = datetime.now()

users = [
    User(1, 'admin', generate_password_hash('admin')),
    User(2, 'team_leader', generate_password_hash('mars123'))
]

jobs = [
    Job(1, "Поиск воды под поверхностью", 2, 20, "5,7")
]

@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users if user.id == int(user_id)), None)

# Маршруты
@app.route('/')
@login_required
def index(title='Список работ'):
    return render_template('jobs/jobs_list.html', jobs=jobs, title=title)

@app.route('/login', methods=['GET', 'POST'])
def login(title='Авторизация'):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = next((user for user in users if user.username == username), None)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('index'))
        
        flash('Неверные учетные данные', 'danger')
    
    return render_template('auth/login.html', title=title)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/jobs/add', methods=['GET', 'POST'])
@login_required
def add_job(title='Добавить новую работу'):
    if request.method == 'POST':
        title = request.form.get('title')
        work_size = request.form.get('work_size')
        collaborators = request.form.get('collaborators')
        is_finished = 'is_finished' in request.form
        
        new_job = Job(
            id=len(jobs) + 1,
            title=title,
            team_leader=current_user.id,
            work_size=work_size,
            collaborators=collaborators,
            is_finished=is_finished
        )
        jobs.append(new_job)
        flash('Работа успешно добавлена', 'success')    
        return redirect(url_for('index'))
    
    return render_template('jobs/add_job.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)