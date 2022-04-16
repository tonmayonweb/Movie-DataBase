from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, validators, SubmitField
import requests
from sqlalchemy import desc

API_KEY = "66f6975cdf45031ac423b530df397a61"
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# THIS IS WTFORM CLASS
class AddMovie(Form):
    movie = StringField('Movie Name', validators=[validators.DataRequired()])
    ok = SubmitField('Submit')


# THIS IS DATABASE CLASS
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.String())
    description = db.Column(db.String(300))
    rating = db.Column(db.Float(10))
    ranking = db.Column(db.Integer())
    review = db.Column(db.String(100))
    img_url = db.Column(db.String(100))


db.create_all()


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg",
# )
#
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    movies_list = db.session.query(Movie).order_by(desc(Movie.rating)).all()
    db.session.commit()
    return render_template("index.html", movies=movies_list)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        movie_id = request.form["id"]
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = request.form["rating"]
        movie_to_update.review = request.form["review"]
        movie_to_update.ranking = request.form["ranking"]
        db.session.commit()
        return redirect(url_for('home'))

    """GET: Renders specific book's editing form page"""

    movie_id = request.args.get('id')

    movie_selected = Movie.query.get(movie_id)
    return render_template("edit.html", movie=movie_selected)


@app.route('/del', methods=['GET', 'POST'])
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/add', methods=["GET", "POST"])
def add():
    form = AddMovie(request.form)
    if request.method == "POST" and form.validate():
        movie_name = form.movie.data
        url = "https://api.themoviedb.org/3/search/movie"
        param = {
            'api_key': API_KEY,
            'query': movie_name,
        }

        movie_search = requests.get(url=url, params=param)
        data = movie_search.json()
        print(len(data["results"]))
        movies_name = [data["results"][x]["original_title"] for x in range(len(data["results"]))]
        movie_id = [data["results"][y]["id"] for y in range(len(data["results"]))]
        release_date = [data["results"][y]["release_date"] for y in range(len(data["results"]))]
        return render_template('select.html', movies=movies_name, mov_id=movie_id, lines=len(data["results"]),
                               date=release_date)
    elif request.args.get('val'):
        mov_id = request.args.get('val')
        movie_data_req = requests.get(f"https://api.themoviedb.org/3/movie/{mov_id}?api_key={API_KEY}")
        movie_data = movie_data_req.json()
        new_movie = Movie(
            title=movie_data["original_title"],
            year=movie_data["release_date"],
            description=movie_data["overview"],
            rating=movie_data["vote_average"],
            ranking=1,
            review="My favourite character was the caller.",
            img_url=f"https://image.tmdb.org/t/p/w500{movie_data['backdrop_path']}",
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
