from flask import(
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import sqlite3


app = Flask(__name__)
app.secret_key = 'naggets123'

product = {}

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('get_log'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper



@app.route('/reg', methods=['GET','POST'])
def get_reg():
    if request.method == 'POST':
        name = request.form.get('login', type=str)
        age = request.form.get('password', type=int)
        
        # Открытие нового соединения для каждого запроса
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()  
        
        return render_template('reg.html', name=name, age=age)
    return render_template('reg.html')


@app.route('/log', methods=['GET','POST'])
def get_log():
    if request.method == 'POST':
        name = request.form.get('login', type=str)
        age = request.form.get('password', type=str)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ? AND age = ?', (name, age))
        user = cursor.fetchone()  
        conn.close()
        
        if user:
            session["login"] = request.form.get('login')
            return redirect(url_for('get_main'))
        else:
            error_message = "Неверный логин или пароль"
            return render_template('log.html', error=error_message)

        

    return render_template('log.html')


@app.route('/', methods=['GET','POST'])
@login_required
def get_main():
    profile=session.get('login', 'Гость')
    if request.method == 'POST':
        
        title = request.form.get('title', type=str)
        price = request.form.get('price', type=int)
        if title and price:
            product[title] = price
        return render_template('index.html', product =product, profile=profile)
    return render_template('index.html', product =product, profile=profile)

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('get_main'))



if __name__ == '__main__':
    app.run(debug=True)

