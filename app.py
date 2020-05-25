from flask import Flask, render_template, request, redirect, url_for
import requests, math
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import SubmitField, StringField
# from wtforms.validators import DataRequired


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'mykeyisseceret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class AddForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     submit = SubmitField('Add')


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name



@app.route('/')
def index_get():

    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2a0d4205193503d617df50c6ea042e23'
    weather_data = []
    for city in cities:
        
        resp = requests.get(url.format(city.name)).json()
        print(resp)
        weather = {
            'city': city.name,
            'temperature': math.ceil(resp['main']['temp']) ,
            'description': resp['weather'][0]['description'],
            'icon': resp['weather'][0]['icon'],
            'humidity': resp['main']['humidity'] ,
        }

        weather_data.insert(0,weather)

    # print(weather)
    return render_template('weather.html', weather_data=weather_data)


@app.route('/', methods=['POST'])
def index_post():

    new_city = request.form.get('city')

    if new_city:
        new_city_obj = City(name=new_city)
        db.session.add(new_city_obj)
        db.session.commit()


    # form = AddForm()
    # if form.validate_on_submit():
    #     city = City(form.name.data)
    #     db.session.add(city)
    #     db.session.commit()
    #     form.name.data = ''

    return redirect(url_for('index_get'))


if __name__ == '__main__':
    app.run(debug=True)