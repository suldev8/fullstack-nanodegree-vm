from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Startup, Base, Founder
from flask import Flask, render_template

engine = create_engine('sqlite:///startup.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

@app.route('/')
def home():
    startups = session.query(Startup).all()
    return render_template('home.html', startups=startups)

@app.route('/details/<int:id>')
def details(startup_id):
    
    return render_template('details.html')

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',8000)