import requests
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from gooutsafe import app
from gooutsafe.forms.add_measure import MeasureForm
from gooutsafe.forms.add_stay_time import StayTimeForm
from gooutsafe.forms.add_table import TableForm
from gooutsafe.forms.add_times import TimesForm
from gooutsafe.forms.restaurant import RestaurantForm
from gooutsafe.rao.restaurant_manager import RestaurantManager

restaurants = Blueprint('restaurants', __name__)


@restaurants.route('/my_restaurant', methods=['GET'])
@login_required
def my_restaurant():
    """Given the operator, this method allows him to see the details of his restaurant

    Returns:
        Returns the page of the restaurant's details
    """

    return details(current_user.id)

@restaurants.route('/restaurants/<restaurant_id>')
@login_required
def restaurant_sheet(restaurant_id):
    """This method returns the single page for a restaurant

    Args:
        restaurant_id (int): univocal identifier of the restaurant
    """
    restaurant_sheet = RestaurantManager.get_restaurant_sheet(restaurant_id)
    list_measures = restaurant_sheet['restaurant']['list_measures'].split(',')[1:]
    if restaurant_sheet is None:
        flash('No restaurant found given the specified id')
        return redirect(url_for('home.index'))

    return render_template("restaurantsheet.html",
                           restaurant=restaurant_sheet['restaurant'], list_measures=list_measures,
                           average_rate=restaurant_sheet['average_rate'], max_rate=restaurant_sheet['max_rate'],
                           is_open=restaurant_sheet['is_open']
                           )


@restaurants.route('/restaurants/like/<restaurant_id>')
@login_required
def like_toggle(restaurant_id):
    """Updates the like count

    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Redirects to the single page for a restaurant
    """
    like_toggled = RestaurantManager.put_toggle_like(restaurant_id, current_user.id)
    if not like_toggled:
        flash('Unable to toggle like')
    return restaurant_sheet(restaurant_id)


@restaurants.route('/restaurants/add/<int:id_op>', methods=['GET', 'POST'])
@login_required
def add(id_op):
    """Given an operator, this method allows him to add a restaurant

    Args:
        id_op (int): univocal identifier for the customer

    Returns:
        Redirects the view to the operator's page
    """
    form = RestaurantForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            name = form.data['name']
            address = form.data['address']
            city = form.data['city']
            phone = form.data['phone']
            menu_type = form.data['menu_type']
            json_data_to_send = {
                'name': name,
                'address': address,
                'city': city,
                'phone': phone,
                'menu_type': menu_type,
                'op_id': id_op
            }
            restaurant_added = RestaurantManager.post_add(json_data_to_send)
            if not restaurant_added:
                flash('Something went wrong with the creation of the restaurant, sorry!')
            else:
                return redirect(url_for('auth.operator', op_id=id_op))
    return render_template('create_restaurant.html', form=form)


@restaurants.route('/restaurants/details/<int:id_op>', methods=['GET', 'POST'])
@login_required
def details(id_op):
    """Given an operator, this method allows him to see the details of his restaurant

    Args:
        id_op (int): univocal identifier of the operator

    Returns:
        Returns the page of the restaurant's details
    """
    table_form = TableForm()
    time_form = TimesForm()
    measure_form = MeasureForm()
    avg_time_form = StayTimeForm()

    json_data = RestaurantManager.get_restaurant_by_op_id(id_op)
    if not json_data:
        return redirect(url_for('restaurants.add', id_op=id_op))
    restaurant = json_data['restaurant']
    list_measures = restaurant['list_measures'].split(',')[1:]

    return render_template('add_restaurant_details.html',
                           restaurant=restaurant, tables=json_data['tables'],
                           table_form=table_form, time_form=time_form,
                           times=restaurant['availabilities'], measure_form=measure_form,
                           avg_time_form=avg_time_form, avg_stay=restaurant['avg_stay'],
                           list_measure=list_measures)


@restaurants.route('/restaurants/save/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_details(id_op, rest_id):
    """This method gives the operator the possibility to add tables to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    table_form = TableForm()

    if request.method == "POST":
        if table_form.is_submitted():
            num_tables = table_form.data['number']
            capacity = table_form.data['max_capacity']

            json_data = {'number': num_tables, 'max_capacity': capacity}
            tables_added = RestaurantManager.post_add_tables(rest_id, json_data)
            if not tables_added:
                flash('Error in saving the tables')

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/savetime/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_time(id_op, rest_id):
    """This method gives the operator the possibility to add opening hours to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    time_form = TimesForm()
    if request.method == "POST":
        if time_form.is_submitted():
            day = time_form.data['day']
            start_time = time_form.data['start_time']
            end_time = time_form.data['end_time']

            json_data_to_send = {'day': day,
                                    'start_time': str(start_time),
                                    'end_time': str(end_time)}
            avail_added = RestaurantManager.post_add_time(rest_id, json_data_to_send) 
            if not avail_added:
                flash('Error in saving the availability')

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/savemeasure/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_measure(id_op, rest_id):
    """This method gives the operator the possibility to add precaution meausures 
    to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    measure_form = MeasureForm()

    if request.method == "POST":
        if measure_form.is_submitted():
            measure = measure_form.data['measure']
            json_data_to_send = {'measure': measure}
            measure_added = RestaurantManager.put_add_measure(rest_id, json_data_to_send)
            if not measure_added:
                flash('Error in saving the measure')
    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/avgstay/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_avg_stay(id_op, rest_id):
    avg_time_form = StayTimeForm()

    if request.method == "POST":
        if avg_time_form.validate_on_submit():
            hours = avg_time_form.data['hours']
            minute = avg_time_form.data['minutes']
            json_data_to_send = {'hours': hours,
                                'minutes': minute}
            avg_stay_added = RestaurantManager.put_add_avg_stay(rest_id, json_data_to_send)
            if avg_stay_added:
                flash('Error in saving the average stay time')

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/edit_restaurant/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def edit_restaurant(id_op, rest_id):
    """This method allows the operator to edit the information about his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    form = RestaurantForm()
    if request.method == "POST":
        if form.is_submitted():
            name = form.data['name']
            address = form.data['address']
            city = form.data['city']
            phone = form.data['phone']
            menu_type = form.data['menu_type']
            json_data_to_send = {'name': name,
                                    'address': address,
                                    'city': city,
                                    'phone': phone,
                                    'menu_type': menu_type}
            restaurant_edited = RestaurantManager.put_edit_restaurant(rest_id, json_data_to_send)
            if restaurant_edited:
                flash('Error in saving the average stay time')
            else:
                return redirect(url_for('auth.operator', op_id=id_op))

    return render_template('update_restaurant.html', form=form)
