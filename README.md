Restaurant Menu Application
============================
This web application allows you to browse and add/modify/delete restaurants and their corresponding menu items.

It contains the following files
-------------------------------
1. **database_setup.py:**
	This file contains the data entities and its corresponding ORM configurations.

2. **finalProject.py:**
	This is the main file which implements the administration of the restaurants and their menus.

3. **templates/*.html:**
	Multiple html templates which render the UI for different functionalities in the browser.

4. **static/styles.css:**
	This file contains the CSS/Styling for this web application

5. **restaurantmenu.db:**
	This is the database file

6. **README.md**


How to run the application
---------------------------
You need to have `python 2.7.6` and `SqlAlchemy 0.8.4` installed on your machine.

1. In terminal/cmd, navigate to the directory where the files are located.
2. Run the command line `python finalProject.py` which will run the web application on port `5000`.
3. Open the browser and go to `http://localhost:5000/`, this will open the restaurant menu application.
4. You should be able to add/edit/modify restaurants and their corresponding menu items.
5. API Endpoints:
	1. Get all restaurants: `http://localhost:5000/restaurants/JSON`
	2. Get all menu items of a given restaurant: `http://localhost:5000/restaurant/{restaurant_id}/menu/JSON`
	3. Get a particular menu item: `http://localhost:5000/restaurant/{restaurant_id}/menu/{menu_id}/JSON`
