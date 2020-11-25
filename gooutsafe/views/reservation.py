from datetime import datetime
from datetime import timedelta

from flask import Blueprint, redirect, render_template, request, url_for, flash, abort
# from flask_user import roles_required
from flask_login import current_user, login_required

from gooutsafe.forms.filter_form import FilterForm
from gooutsafe.forms.reservation import ReservationForm

from gooutsafe.rao.reservation_manager import ReservationManager
from gooutsafe.rao.restaurant_manager import RestaurantManager
from gooutsafe.rao.user_manager import UserManager


reservation = Blueprint('reservation', __name__)

@reservation.route('/create_reservation/<restaurant_id>', methods=['GET', 'POST'])
def create_reservation(restaurant_id):
    """This method allows the customer to create a new reservation, on a specific restaurant,
    depending on its opening hours and the available tables

    Args:
        restaurant_id (int): univocal identifier of the restaurant
    
    """
    restaurant_id = int(restaurant_id)
    if current_user.type == 'customer':
        _,_,details = ReservationManager.get_restaurant_detatils(restaurant_id)
        restaurant = details['restaurant']
        restaurant_name = restaurant['name']
        form = ReservationForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                start_date = form.data['start_date']
                start_time = form.data['start_time']
                people_number = form.data['people_number']
                start_time_merged = datetime.combine(start_date, start_time)
                str_start_time = datetime.strftime(start_time_merged, "%Y-%m-%d %H:%M:%S")
                user_id = current_user.id
                response = ReservationManager.create_reservation(restaurant_id, user_id, str_start_time, people_number)
                if response.status_code != 200:
                    flash("There aren't free tables for that hour or the restaurant is close")
                    return redirect('/restaurants/' + str(restaurant_id))
                else:
                    return redirect(url_for('auth.profile', id=current_user.id))
            else:
                flash("Take a look to the inserted data")
        return render_template('create_reservation.html', restaurant_name=restaurant_name, form=form)
    return redirect(url_for('home.index'))



@reservation.route('/reservations/<restaurant_id>', methods=['GET', 'POST'])
def reservation_all(restaurant_id):
    """Returns the whole list of reservations, given a restaurant.
    It also gives to the operator the opportunity to filter reservations
    by date, so it's possible to count people.

    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        The template of the reservations.
    """
    filter_form = FilterForm()
    response = ReservationManager.get_all_reservation_restaurant(restaurant_id)
    if response.status_code != 200:
        flash("There are no reservations")
        restaurant = {}
        reservations = {}
        people = 0
        return render_template("restaurant_reservation.html",
                                restaurant=restaurant, reservations=reservations,
                                filter_form=filter_form, people=people)
    json_resp = response.json()
    reservations = json_resp['reservations']
    _, _, json_details = ReservationManager.get_restaurant_detatils(restaurant_id)
    restaurant = json_details['restaurant']
    
    users = []
    people = 0
    if reservations:
        for r in reservations:
            start_time = datetime.strptime(r['start_time'], "%Y-%m-%dT%H:%M:%SZ")
            r['start_time'] = datetime.strftime(start_time, "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(r['end_time'], "%Y-%m-%dT%H:%M:%SZ")
            r['end_time'] = datetime.strftime(end_time, "%Y-%m-%d %H:%M")
            user_dict = {}
            user_id = r['user_id']
            user = UserManager.get_user_by_id(user_id)
            r['lastname'] = user.extra_data['lastname']
            if r['is_confirmed']:
                people = people + r['people_number']

    if request.method == 'POST':
        if filter_form.is_submitted():
            filter_date = filter_form.data['filter_date']
            start_time = filter_form.data['start_time']
            end_time = filter_form.data['end_time']

            if filter_date is not None and start_time is not None and end_time is not None:
                start_date_time = datetime.combine(filter_date, start_time)
                end_date_time = datetime.combine(filter_date, end_time)
                start_date_time = datetime.strftime(start_date_time,"%Y-%m-%d %H:%M:%S")
                end_date_time = datetime.strftime(end_date_time,"%Y-%m-%d %H:%M:%S")
                response = ReservationManager.filtered_reservations(
                    restaurant_id, start_date_time, end_date_time
                )
                json_resp = response.json()
                reservations = json_resp['reservations']

                return render_template("restaurant_reservation.html",
                                       restaurant=restaurant, reservations=reservations,
                                       filter_form=filter_form, people=people)
            else:
                flash("The inserted data are not valid")
    return render_template("restaurant_reservation.html",
                           restaurant=restaurant, reservations=reservations,
                           filter_form=filter_form, people=people)


@reservation.route('/reservation/delete/<restaurant_id>/<reservation_id>', methods=['GET', 'POST'])
def delete_reservation(reservation_id, restaurant_id):
    """Given a customer and a reservation id,
    this function delete the reservation from the database.

    Args:
        id (int): univocal identifier for the reservation

    Returns:
        Redirects the view to the customer profile page.
    """
    response = ReservationManager.delete_reservation(reservation_id)
    if response.status_code != 200:
        flash("Error during deletion")
        
    if current_user.type == 'customer':
        return redirect(url_for('auth.profile', id=current_user.id))
    else:
        return redirect(url_for('reservation.reservation_all',restaurant_id=restaurant_id))



@reservation.route('/reservation/edit/<restaurant_id>/<reservation_id>', methods=['GET', 'POST'])
def edit_reservation(restaurant_id, reservation_id):
    """Allows the customer to edit a single reservation,
    if there's an available table within the opening hours
    of the restaurant.

    Args:
        reservation_id (int): univocal identifier of the reservation
        customer_id (int): univocal identifier of the customer

    Returns:
        Redirects the view to the customer profile page.
    """
    form = ReservationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            start_date = form.data['start_date']
            start_time = form.data['start_time']
            people_number = form.data['people_number']
            start_time_merged = datetime.combine(start_date, start_time)
            str_start_time = datetime.strftime(start_time_merged, "%Y-%m-%d %H:%M:%S")
            response = ReservationManager.edit_reservation(reservation_id, restaurant_id, str_start_time, people_number)
            if response.status_code != 200:
                flash("There aren't free tables for that hour or the restaurant is close")
            else:
                flash("Reservation successfully updated")
    return redirect(url_for('auth.profile', id=current_user.id))


@reservation.route('/reservation/confirm/<int:restaurant_id>/<int:reservation_id>')
def confirm_reservation(restaurant_id, reservation_id):
    """
    This method is used to confirm reservation

    Args:
        restaurant_id (Integer): the restaurant id of the reservation

    Returns:
        redirect: redirects to the reservations operator page
    """
    response = ReservationManager.confirm_reservation(reservation_id)
    if response.status_code != 200:
        flash('Error during confermation')
    return redirect(url_for('reservation.reservation_all',restaurant_id=restaurant_id))


@reservation.route('/my_reservations')
def my_reservations():
    """Given a restaurant operator, this method returns all its reservations

    """
    restaurant = RestaurantManager.get_restaurant_by_op_id(current_user.id)
    if restaurant is None:
        from gooutsafe.views.restaurants import add
        return add(current_user.id)
    restaurant_id = restaurant['restaurant']['id']
    return reservation_all(restaurant_id)
