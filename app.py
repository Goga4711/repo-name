from flask import Flask, render_template, request, redirect, url_for, session, flash 
import sqlite3  
import hashlib 

# Инициализация Flask приложения
app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Секретный ключ для сессий

# Путь к базе данных
DATABASE = 'users.db'

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DATABASE)  # Подключение к SQLite
    conn.row_factory = sqlite3.Row  # Устанавливаем формат данных как строки
    return conn

# Маршрут для страницы авторизации
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Если форма отправлена
        username = request.form['username']  # Получаем введенное имя пользователя
        password = hashlib.md5(request.form['password'].encode()).hexdigest()  # Хэшируем пароль
        conn = get_db_connection()  # Подключение к базе данных
        # Проверка существования пользователя в базе данных
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()  # Закрываем соединение с базой
        if user:  # Если пользователь найден
            session['user'] = username  # Сохраняем пользователя в сессии
            return redirect(url_for('manage'))  # Перенаправляем на страницу управления
        else:
            flash('Invalid username or password')  # Сообщение об ошибке
    return render_template('login.html')  # открываем страницу логина

# Маршрут для страницы управления пользователями
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if 'user' not in session:  # Если пользователь не авторизован
        return redirect(url_for('login'))  # Перенаправляем на логин

    conn = get_db_connection()  # Подключение к базе данных
    users = conn.execute('SELECT * FROM users').fetchall()  # Получаем всех пользователей из базы

    if request.method == 'POST':  # Если форма отправлена
        action = request.form.get('action')  # Получаем действие (insert, update, delete)
        username = request.form.get('username')  # Получаем имя пользователя
        password = request.form.get('password')  # Получаем пароль

        if action == 'insert':  # Если добавление
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                         (username, hashlib.md5(password.encode()).hexdigest()))
        elif action == 'update':  # Если обновление
            conn.execute('UPDATE users SET password = ? WHERE username = ?', 
                         (hashlib.md5(password.encode()).hexdigest(), username))
        elif action == 'delete':  # Если удаление
            conn.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()  # Сохраняем изменения
        return redirect(url_for('manage'))  # Обновляем страницу

    conn.close()  # Закрываем соединение с базой
    return render_template('manage.html', users=users)  # Рендерим страницу управления

# Маршрут для выхода из системы
@app.route('/logout')
def logout():
    session.pop('user', None)  # Удаляем пользователя из сессии
    return redirect(url_for('login'))  # Перенаправляем на логин

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)  # Режим отладки
