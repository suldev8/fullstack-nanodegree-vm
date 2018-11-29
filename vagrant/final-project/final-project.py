from flask import Flask, render_template,request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')

sessionDB = sessionmaker(bind=engine)
session = sessionDB()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new/', methods=['POST', 'GET'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    elif request.method == 'GET':
        return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['POST', 'GET'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['POST', 'GET'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['submit']:
            session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', items=items, restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['POST', 'GET'])
def newItem(restaurant_id):
    if request.method == 'POST':
        item = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant_id
        )
        item.name = request.form['name']
        session.add(item)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newItem.html')

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods=['POST', 'GET'])
def editItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        item.name=request.form['name']
        item.description=request.form['description']
        item.price=request.form['price']
        item.course=request.form['course']
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editItem.html', item=item)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['POST', 'GET'])
def deleteItem(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['submit']:
            session.delete(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteItem.html', item=item)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)