from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Restaurant, MenuItem
from sqlalchemy import asc
from . import db
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import elevenSeventeen, landscape

main = Blueprint('main', __name__)

# Show all restaurants


@main.route('/')
@main.route('/restaurant/')
def showRestaurants():
    restaurants = db.session.query(Restaurant).order_by(asc(Restaurant.name))
    return render_template('restaurants.html', restaurants=restaurants)

# show searched restaurants


@main.route('/search')
def search_restaurants():
    q = request.args.get("q")
    filtered_restaurants = Restaurant.query.filter(
        Restaurant.name.ilike(f"%{q}%")).order_by(asc(Restaurant.name))
    return render_template('restaurantsearch.html', restaurants=filtered_restaurants)

# Create a new restaurant


@main.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        db.session.add(newRestaurant)
        flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        db.session.commit()
        return redirect(url_for('main.showRestaurants'))
    else:
        return render_template('newRestaurant.html')

# Edit a restaurant


@main.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = db.session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('main.showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


# Delete a restaurant
@main.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = db.session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        db.session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        db.session.commit()
        return redirect(url_for('main.showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)

# Show a restaurant menu


@main.route('/restaurant/<int:restaurant_id>/')
@main.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu.html', items=items, restaurant=restaurant)

# Generates a PDF version of the Menu


@main.route('/print_pdf/<int:restaurant_id>')
def print_pdf(restaurant_id):
    # Generate menu data from SQLdatabase
    menu_data = db.session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    restaurant = db.session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    generate_pdf(restaurant.name, menu_data)
    return redirect(url_for('main.showMenu', restaurant_id=restaurant_id))


# Create a new menu item
@main.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'],
                           price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        db.session.add(newItem)
        db.session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('main.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit a menu item


@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):

    editedItem = db.session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    editedItem = db.session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        db.session.add(editedItem)
        db.session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('main.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('main.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)

# Function that generates and styles the PDF


def generate_pdf(restaurant_name, menu_items):
    # Creates the pdf variable which is a canvas that's landscape and a slightly larger than A4 document
    pdf = canvas.Canvas("menu.pdf", pagesize=landscape(elevenSeventeen))
    # Background and segments of the menu
    pdf.setTitle(f"{restaurant_name} Menu")
    pdf.setFillColorRGB(0.75, 0.96, 0.85)
    pdf.rect(0, 680, 1225, 400, fill=1)
    pdf.setFillColorRGB(0.4, 0.4, 0.4)
    pdf.rect(0, 0, 1225, 680, fill=1)
    pdf.setStrokeColorRGB(0.75, 0.96, 0.85)
    pdf.setLineWidth(4)
    pdf.line(330, 670, 330, 50)
    pdf.line(630, 670, 630, 50)
    pdf.line(930, 670, 930, 50)

    # Header of the menu
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Courier-Bold", 28)
    pdf.drawCentredString(600, 750, "Menu")
    pdf.drawCentredString(600, 710, f"{restaurant_name}")

    # Body of the menu
    # Appertizers segment
    pdf.setFillColorRGB(255, 255, 255)
    pdf.setFont("Helvetica-Bold", 20)
    y = 600
    pdf.drawString(50, 650, "Appetizers:")
    pdf.setFont("Helvetica-Bold", 14)
    for item in menu_items:
        if item.course == "Appetizer":
            pdf.setFillColorRGB(0.97, 0.84, 0.56)
            pdf.drawString(280, y, f"{item.price}")
            pdf.setFillColorRGB(255, 255, 255)
            # Creates new line if over 25 characters long
            if len(item.name) > 25:
                index = item.name[:25].rindex(' ')
                pdf.drawString(50, y, f"• {item.name[:index].strip()}")
                item.name = item.name[index:]
                y -= 20
                pdf.drawString(350, y, f"{item.name}")
            else:
                pdf.drawString(50, y, f"• {item.name}")
            y -= 20
    y = 600
    # Entrees Segment
    pdf.setFillColorRGB(255, 255, 255)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(435, 650, "Entrees:")
    pdf.setFont("Helvetica-Bold", 14)
    for item in menu_items:
        if item.course == "Entree":
            pdf.setFillColorRGB(0.97, 0.84, 0.56)
            pdf.drawString(580, y, f"{item.price}")
            pdf.setFillColorRGB(255, 255, 255)
            # Creates new line if over 25 characters long
            if len(item.name) > 25:
                index = item.name[:25].rindex(' ')
                pdf.drawString(350, y, f"• {item.name[:index].strip()}")
                item.name = item.name[index:]
                y -= 20
                pdf.drawString(350, y, f"{item.name}")
            else:
                pdf.drawString(350, y, f"• {item.name}")
            y -= 20
    y = 600
    # Desserts Segment
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColorRGB(255, 255, 255)
    pdf.drawString(730, 650, "Desserts:")
    pdf.setFont("Helvetica-Bold", 14)
    for item in menu_items:
        if item.course == "Dessert":
            pdf.setFillColorRGB(0.97, 0.84, 0.56)
            pdf.drawString(880, y, f"{item.price}")
            pdf.setFillColorRGB(255, 255, 255)
            # Creates new line if over 25 characters long
            if len(item.name) > 25:
                index = item.name[:25].rindex(' ')
                pdf.drawString(650, y, f"• {item.name[:index].strip()}")
                item.name = item.name[index:]
                y -= 20
                pdf.drawString(650, y, f"{item.name}")
            else:
                pdf.drawString(650, y, f"• {item.name}")
            y -= 20
    y = 600
    # Beverages Segment
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColorRGB(255, 255, 255)
    pdf.drawString(1010, 650, "Beverages:")
    pdf.setFont("Helvetica-Bold", 14)
    for item in menu_items:
        if item.course == "Beverage":
            pdf.setFillColorRGB(0.97, 0.84, 0.56)
            pdf.drawString(1180, y, f"{item.price}")
            pdf.setFillColorRGB(255, 255, 255)
            # Creates new line if over 25 characters long
            if len(item.name) > 25:
                index = item.name[:25].rindex(' ')
                pdf.drawString(950, y, f"• {item.name[:index].strip()}")
                item.name = item.name[index:]
                y -= 20
                pdf.drawString(950, y, f"{item.name}")
            else:
                pdf.drawString(950, y, f"• {item.name}")
            y -= 20
    pdf.save()
    print("PDF Generated")
