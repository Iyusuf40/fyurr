#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import date
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    store = []
    data = Par_venue.query.all() ###################
    for _ in data:
        store.append({
            "city" : _.city,
            "state" : _.state,
            "venues" : _.venue
        })
    return render_template('pages/venues.html', areas=store);

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    res = request.form.get('search_term', '')
    item = Venue.query.filter(Venue.name.ilike("%" + res + "%")).all()
    response={
        "count": len(item),
        "data": item
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    store = {}
    u_show = []
    p_show = []
    data = Venue.query.filter(Venue.id == int(venue_id)).first()
    _ = Venue.query.filter(Venue.id == int(venue_id)).first()
    upcoming_shows = Show.query.filter(Show.start_time < datetime.now()).filter(Show.venue_id==_.id).all()
    if len(upcoming_shows):
      for item in upcoming_shows:
          u_show.append({
          "artist_id" : upcoming_shows[0].artist.id,
          "artist_name" : upcoming_shows[0].artist.name,
          "artist_image_link" : upcoming_shows[0].artist.image_link,
          "start_time" : str(item.start_time)
          })
    past_shows = Show.query.filter(Show.start_time > datetime.now()).filter(Show.venue_id==_.id).all()
    if len(past_shows):
      for item in past_shows:
          p_show.append({
          "artist_id" : past_shows[0].artist.id,
          "artist_name" : past_shows[0].artist.name,
          "artist_image_link" : past_shows[0].artist.image_link,
          "start_time" : str(item.start_time)
          })
    store = {
      "id": _.id,
      "name": _.name,
      "genres": _.genres,
      "address" : _.address,
      "city": _.city,
      "state": _.state,
      "phone": str(_.phone),
      "website": _.website_link,
      "facebook_link": _.facebook_link,
      "seeking_talent": _.seeking_talent,
      "seeking_description": _.seeking_description,
      "image_link": _.image_link,
      "past_shows": p_show,
      "upcoming_shows": u_show,
      "past_shows_count": len(p_show),
      "upcoming_shows_count": len(u_show)
    }
    return render_template('pages/show_venue.html', venue=store)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        form = VenueForm(request.form)
        par_venue = Par_venue.query.filter(Par_venue.city==form.city.data).all()

        if len(par_venue) == True:
            par_venue_id = int(par_venue[0].id)
        else:
            par_venue = Par_venue(city=form.city.data, state=form.state.data)
            db.session.add(par_venue)
            db.session.commit()
            par_venue = Par_venue.query.filter(Par_venue.city==form.city.data).all()
            par_venue_id = int(par_venue[0].id)
        new_venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
        address=form.address.data, phone=form.phone.data, genres=form.genres.data,
        image_link=form.image_link.data, facebook_link=form.facebook_link.data,
        website_link=form.website_link.data, seeking_description=form.seeking_description.data,
        seeking_talent=form.seeking_talent.data, par_venue_id=par_venue_id)

        db.session.add(new_venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

  # on successful db insert, flash success
    if error == False:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term=request.form.get('search_term', '')
    item = Artist.query.filter(Artist.name.ilike("%" + search_term + "%")).all()
    response={
        "count": len(item),
        "data": item
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    store = {}
    u_show = []
    p_show = []
    # data = Artist.query.filter(Artist.id==artist_id).first()
    _ = Artist.query.filter(Artist.id==artist_id).first()
    upcoming_shows = Show.query.filter(Show.start_time < datetime.now()).filter(Show.artist_id==_.id).all()
    if len(upcoming_shows):
      for item in upcoming_shows:
          u_show.append({
          "venue_id" : upcoming_shows[0].venue.id,
          "venue_name" : upcoming_shows[0].venue.name,
          "venue_image_link" : upcoming_shows[0].venue.image_link,
          "start_time" : str(item.start_time)
          })

    past_shows = Show.query.filter(Show.start_time > datetime.now()).filter(Show.artist_id==_.id).all()
    if len(past_shows):
      for item in past_shows:
          p_show.append({
          "venue_id" : past_shows[0].venue.id,
          "venue_name" : past_shows[0].venue.name,
          "venue_image_link" : past_shows[0].venue.image_link,
          "start_time" : str(item.start_time)
          })

    store = {
      "id": _.id,
      "name": _.name,
      "genres": _.genres,
      "city": _.city,
      "state": _.state,
      "phone": str(_.phone),
      "website": _.website_link,
      "facebook_link": _.facebook_link,
      "seeking_venue": _.seeking_venue,
      "seeking_description": _.seeking_description,
      "image_link": _.image_link,
      "past_shows": p_show,
      "upcoming_shows": u_show,
      "past_shows_count": len(p_show),
      "upcoming_shows_count": len(u_show)
    }
    return render_template('pages/show_artist.html', artist=store)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter(Artist.id==artist_id).first()
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist = Artist.query.filter(Artist.id==artist_id).all()[0]
    artist.name=form.name.data; artist.city=form.city.data; artist.state=form.state.data;
    artist.phone=form.phone.data; artist.genres=form.genres.data;
    artist.image_link=form.image_link.data; artist.facebook_link=form.facebook_link.data;
    artist.website_link=form.website_link.data; artist.seeking_description=form.seeking_description.data;
    artist.seeking_venue=form.seeking_venue.data
    db.session.commit()

    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter(Venue.id==venue_id).first()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    par_venue = Par_venue.query.filter(Par_venue.city==form.city.data).all()

    if len(par_venue) == True:
        par_venue_id = int(par_venue[0].id)
    else:
        par_venue = Par_venue(city=form.city.data, state=form.state.data)
        db.session.add(par_venue)
        db.session.commit()
        par_venue = Par_venue.query.filter(Par_venue.city==form.city.data).all()
        par_venue_id = int(par_venue[0].id)

    venue = Venue.query.filter(Venue.id==venue_id).first()

    venue.name=form.name.data; venue.city=form.city.data; venue.state=form.state.data;
    venue.address=form.address.data; venue.phone=form.phone.data; venue.genres=form.genres.data;
    venue.image_link=form.image_link.data; venue.facebook_link=form.facebook_link.data;
    venue.website_link=form.website_link.data; venue.seeking_description=form.seeking_description.data;
    venue.seeking_talent=form.seeking_talent.data; venue.par_venue_id=par_venue_id
    db.session.commit()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        form = ArtistForm(request.form)
        new_artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
        phone=form.phone.data, genres=form.genres.data,
        image_link=form.image_link.data, facebook_link=form.facebook_link.data,
        website_link=form.website_link.data, seeking_description=form.seeking_description.data,
        seeking_venue=form.seeking_venue.data)

        db.session.add(new_artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    if error == False:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  store = []
  data = Show.query.all()
  for _ in data:
      store.append({"venue_id" : _.venue_id,
      "artist_id" : _.artist_id,
      "start_time" : str(_.start_time),
      "venue_name" : _.venue.name,
      "artist_name" : _.artist.name,
      "artist_image_link" : _.artist.image_link
      })
  return render_template('pages/shows.html', shows=store)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
        form = ShowForm(request.form)
        artist_id= int(form.artist_id.data)
        venue_id= int(form.venue_id.data)
        new_show = Show(artist_id=artist_id, venue_id=venue_id,
        start_time=form.start_time.data)
        db.session.add(new_show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    # on successful db insert, flash success
    if error == False:
        flash('Show was successfully listed!')
    else:
        flash('An error occurred. Show could not be listed.')
    # TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
