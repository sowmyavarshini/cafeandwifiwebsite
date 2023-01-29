from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe location on Google Maps(URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image(URL)', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    sockets = StringField('Socket Availability (Yes/No)', validators=[DataRequired()])
    toilet = StringField('Toilet Availability (Yes/No)', validators=[DataRequired()])
    wifi = StringField('Wifi Availability (Yes/No)', validators=[DataRequired()])
    calls = StringField('Can you attend calls (Yes/No)', validators=[DataRequired()])
    seats = StringField('Number of seats available', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


def str_to_bool(argument):
    if argument in ['true', 'True', 'T', 't', 'Yes', 'yes', 'y', 'Y', '1']:
        return True
    else:
        return False


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
                name=request.form.get('name'),
                map_url=request.form.get('map_url'),
                img_url=request.form.get('img_url'),
                location=request.form.get('location'),
                has_sockets=str_to_bool(request.form.get('sockets')),
                has_toilet=str_to_bool(request.form.get('toilet')),
                has_wifi=str_to_bool(request.form.get('wifi')),
                can_take_calls=str_to_bool(request.form.get('calls')),
                seats=request.form.get('seats'),
                coffee_price=request.form.get('coffee_price')

            )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafess = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=cafess)


@app.route('/delete/<int:cafe_id>')
def delete_post(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))


if __name__ == '__main__':
    app.run(debug=True)
