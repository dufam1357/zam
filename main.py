#Импорт
from flask import Flask, render_template, request, redirect, session
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
#Задаем секретный ключ для работы session
app.secret_key = 'my_top_secret_123'
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    subtitle:Mapped[str]
    text:Mapped[str]
    #email владельца карточки
    user_email = db.Column(db.String(100), nullable=False)

    #Инициализация
    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
    
    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Задание №1. Создать таблицу User
class User(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]

#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        #Задание №4. Реализовать проверку пользователей
        users = User.query.all()
        for user in users:
            if user.email == form_login and user.password == form_password:
                session['email'] = user.email
                return redirect('/index')
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        #Задание №3. Реализовать запись пользователей

        user = User(email = email , password = password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    #Задание №4. Сделай, чтобы пользователь видел тольуо свои карточки
    cards = Card.query.filter_by(user_email = session['email']).order_by(Card.id).all()
    return render_template('index.html', cards=cards)

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Задание №4. Сделай, чтобы создание карточки происходило от имени пользователя
        card = Card(title=title, subtitle=subtitle, text=text , user_email = session['email'])

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
