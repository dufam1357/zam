#Импорт
from flask import Flask, render_template,request, redirect
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app )

#Задание №1. Создай таблицу БД
class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    subtitle:Mapped[str]
    text:Mapped[str]








#Запуск страницы с контентом
@app.route('/')
def index():
    #Отображение объектов из БД
    #Задание №2. Отоброзить объекты из БД в index.html
    cards = Card.query.all()

    return render_template('index.html',
                           cards = cards

                           )

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    #Задание №2. Отоброзить нужную карточку по id
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

        #Задание №2. Создайте сопосб записи данных в БД
        card = Card(subtitle = subtitle , text = text , title = title)
        db.session.add(card)
        db.session.commit()




        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)