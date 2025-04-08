from flask import Flask, request, redirect, url_for, render_template
import psycopg2
import re

app = Flask(__name__)

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        port="5432",  # Порт, указанный в docker-compose.yml
        dbname="phonebook",
        user="user",
        password="password"
    )
    return conn

# Проверка формата номера телефона
def is_valid_phone_number(phone_number):
    # Проверяем, что номер состоит из 11 цифр и начинается с +7
    return re.match(r'^\+7\d{10}$', phone_number) is not None

# Главная страница (просмотр всех контактов)
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts;')
    contacts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', contacts=contacts)

# Добавление нового контакта
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        note = request.form.get('note', '').strip()

        # Проверка, что имя и номер телефона не пусты
        if not full_name or not phone_number:
            return render_template('create.html', error=True, full_name=full_name, phone_number=phone_number)

        # Проверка формата номера телефона
        if not is_valid_phone_number(phone_number):
            return render_template('create.html', error=True, full_name=full_name, phone_number=phone_number,
                                 error_message="Номер телефона должен быть в формате +79876543210 и содержать 11 цифр.")

        # Проверка уникальности номера телефона
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id FROM contacts WHERE phone_number = %s', (phone_number,))
        existing_contact = cur.fetchone()

        if existing_contact:
            cur.close()
            conn.close()
            return render_template('create.html', error=True, full_name=full_name, phone_number=phone_number,
                                 error_message="Номер телефона уже существует.")

        # Вставка нового контакта
        cur.execute('INSERT INTO contacts (full_name, phone_number, note)'
                    'VALUES (%s, %s, %s)',
                    (full_name, phone_number, note))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# Редактирование контакта
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Получаем данные текущего контакта
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    contact = cur.fetchone()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        note = request.form.get('note', '').strip()

        # Проверка, что имя и номер телефона не пусты
        if not full_name or not phone_number:
            return render_template('edit.html', error=True, full_name=full_name, phone_number=phone_number, contact=contact)

        # Проверка формата номера телефона
        if not is_valid_phone_number(phone_number):
            return render_template('edit.html', error=True, full_name=full_name, phone_number=phone_number,
                                 error_message="Номер телефона должен быть в формате +79876543210 и содержать 11 цифр.", contact=contact)

        # Проверка уникальности номера телефона (исключая текущий контакт)
        cur.execute('SELECT id FROM contacts WHERE phone_number = %s AND id != %s', (phone_number, id))
        existing_contact = cur.fetchone()

        if existing_contact:
            cur.close()
            conn.close()
            return render_template('edit.html', error=True, full_name=full_name, phone_number=phone_number,
                                 error_message="Номер телефона уже существует.", contact=contact)

        # Обновление контакта
        cur.execute('UPDATE contacts SET full_name = %s, phone_number = %s, note = %s'
                    'WHERE id = %s',
                    (full_name, phone_number, note, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    
    cur.close()
    conn.close()
    return render_template('edit.html', contact=contact)

# Удаление контакта
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)