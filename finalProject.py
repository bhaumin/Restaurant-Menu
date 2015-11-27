from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# 1. Show All Restaurants
@app.route('/')
@app.route('/restaurants')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)


# 2. Create New Restaurant
@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():

	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New restaurant created successfully!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('newrestaurant.html')


# 3. Edit a Restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurantToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			restaurantToEdit.name = request.form['name']
		session.add(restaurantToEdit)
		session.commit()
		flash("Restaurant edited successfully!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = restaurantToEdit)

# 4. Delete a Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		flash("Restaurant deleted successfully!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant = restaurantToDelete)


# 5. Show Restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return render_template('menu.html', restaurant = restaurant, items = items)


# 6. Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):

	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New item created successfully!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)


# 7. Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Item edited successfully!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


# 8. Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Item deleted successfully!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToDelete)



# Making an API Endpoint (GET Request) for all menu items
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


# Making an API Endpoint (GET Request) for the requested menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def getMenuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	return jsonify(MenuItem=item.serialize)



if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
