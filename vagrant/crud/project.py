from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine
sessionDB = sessionmaker(bind=engine)
session = sessionDB()


app = Flask(__name__)


@app.route("/restaurants/<int:restaurant_id>/")
def menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route("/restaurants/<int:restaurant_id>/json")
def menuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

@app.route("/restaurants/<int:restaurant_id>/<int:item_id>/json")
def menuItemJson(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id, restaurant_id=restaurant_id).one()
    return jsonify(MenuItem=item.serialize)


@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], price=request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('new item added')
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    if request.method == 'GET':
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/<int:item_id>/edit/", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    editItem = session.query(MenuItem).filter_by(id=item_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        session.add(editItem)
        session.commit()
        flash('menu item edited')
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, item=editItem)


@app.route("/restaurants/<int:restaurant_id>/<int:item_id>/delete/", methods=['POST', 'GET'])
def deleteMenuItem(restaurant_id, item_id):
    deleteItem = session.query(MenuItem).filter_by(id=item_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash('menu item deleted')
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('deleteMenuItem.html', item=deleteItem)
if __name__ == "__main__":
    app.secret_key = 'super_key'
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
