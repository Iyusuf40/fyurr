app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"),
                nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"),
                nullable=False)


class Par_venue(db.Model):
    __tablename__ = "Par_venue"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venue = db.relationship("Venue", backref="par_venue", lazy=True)
    # venue = db.Column(db.Integer, db.ForeignKey("Venue.id"),
    #             nullable=False)



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    address = db.Column(db.String())
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    par_venue_id =  db.Column(db.Integer, db.ForeignKey("Par_venue.id"),
                nullable=False)
    show = db.relationship("Show", backref="venue", lazy=True)
    # par_venue = db.relationship("Par_venue", backref="par_venue", lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    show = db.relationship("Show", backref="artist", lazy=True)
