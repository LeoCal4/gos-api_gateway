import requests
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from gooutsafe import app
from gooutsafe.forms import LoginForm
from gooutsafe.forms.authority import AuthorityForm
from gooutsafe.forms.filter_form import FilterForm
from gooutsafe.forms.reservation import ReservationForm
from gooutsafe.forms.update_customer import AddSocialNumberForm
from gooutsafe.rao.user_manager import UserManager
from gooutsafe.rao.restaurant_manager import RestaurantManager
from gooutsafe.rao.reservation_manager import ReservationManager
from gooutsafe.rao.notification_tracing_manager import NotificationTracingManager as ntm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(re=False):
    """Allows the user to log into the system

    Args:
        re (bool, optional): boolean value that describes whenever
        the user's session is new or needs to be reloaded. Defaults to False.

    Returns:
        Redirects the view to the personal page of the user
    """
    form = LoginForm()

    if form.is_submitted():
        email, password = form.data['email'], form.data['password']
        user = UserManager.authenticate_user(email, password)
        if user is None:
            # user is not authenticated
            flash('Invalid credentials')
        else:
            # user is authenticated
            login_user(user)

            if user.type == 'operator':
                return redirect(url_for('auth.operator', op_id=user.id))
            elif user.type == 'customer':
                return redirect(url_for('auth.profile', id=user.id))
            else:
                return redirect('/authority/%d/0' % user.id)

    return render_template('login.html', form=form, re_login=re)


@auth.route('/relogin')
def re_login():
    """Method that is being called after the user's session is expired.

    """
    return login(re=True)


@auth.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    """This method allows the customer to see its personal page

    Args:
        id (int): univocal identifier of the customer

    Returns:
        Redirects the view to personal page of the customer
    """

    if current_user.id == id:
        form = ReservationForm()
        social_form = AddSocialNumberForm()

        # restaurants = RestaurantManager.retrieve_all()
        resp = ReservationManager.get_all_reservation_customer(id)
        if resp.status_code != 200:  
            return render_template('customer_profile.html',social_form=social_form)      

        json_response = resp.json()
        restaurants = []
        reservations = json_response['reservations']
        for res in reservations:
            #time reformat
            start_time = datetime.strptime(res['start_time'], "%Y-%m-%dT%H:%M:%SZ")
            res['start_time'] = datetime.strftime(start_time, "%Y-%m-%d %H:%M")
            print()
            #restaurant details extraction
            rest_dict = {}
            restaurant_id = res['restaurant_id']
            _,_,details = ReservationManager.get_restaurant_detatils(restaurant_id)
            restaurant = details['restaurant']
            rest_dict['name'] = restaurant['name']
            rest_dict['address'] = restaurant['address']
            restaurants.append(rest_dict)
        
        return render_template('customer_profile.html',
            reservations=reservations, restaurants=restaurants,
            form=form, social_form=social_form)

    return redirect(url_for('home.index'))


@auth.route('/operator/<int:op_id>', methods=['GET', 'POST'])
@login_required
def operator(op_id):
    """This method allows the operator to access the page of its personal info

    Args:
        id (int): univocal identifier of the operator

    Returns:
        Redirects the view to personal page of the operator
    """

    if current_user.id == op_id:
        filter_form = FilterForm()
        json_data = RestaurantManager.get_restaurant_details(op_id)
        if json_data is None:
            restaurant = None
        else:
            restaurant = json_data['details']['restaurant']

        return render_template('operator_profile.html',
                        restaurant=restaurant, filter_form=filter_form)
    return redirect(url_for('home.index'))


@auth.route('/authority/<int:id>/<int:positive_id>', methods=['GET', 'POST'])
@login_required
def authority(id, positive_id):
    """This method allows the Health Authority to see its personal page.

    Args:
        id (int): the univocal identifier for the Health Authority
        positive_id (int): the identifier of the positive user

    Returns:
        Redirects to the page of the Health Authority
    """
    if current_user.id == id:
        ha_form = AuthorityForm()
        pos_customers = UserManager.get_all_positive_customer()
        if positive_id != 0:
            search_customer = UserManager.get_user_by_id(positive_id)
        else: #authority clicks on "Profile"
            search_customer = None
        return render_template('authority_profile.html',
                               form=ha_form, pos_customers=pos_customers,
                               search_customer=search_customer)
    return redirect(url_for('home.index'))


@auth.route('/logout')
@login_required
def logout():
    """This method allows the users to log out of the system

    Returns:
        Redirects the view to the home page
    """
    logout_user()
    return redirect(url_for('home.index'))


@auth.route('/notifications', methods=['GET'])
@login_required
def notifications():
    """[summary]

    Returns:
        [type]: [description]
    """
    #get all notifications from the manager
    notifications = ntm.retrieve_by_target_user_id(user_id=current_user.id)
    print(notifications)
    processed_notification_info = []
    if current_user.type == "customer":
        for notification in notifications:
            restaurant_name = RestaurantManager.get_restaurant_sheet(notification['contagion_restaurant_id'])['restaurant']['name']
            processed_notification_info.append({"timestamp": notification['timestamp'],
                                                "contagion_datetime": notification['contagion_datetime'],
                                                "contagion_restaurant_name": restaurant_name})
        return render_template('customer_notifications.html', current_user=current_user,
                               notifications=processed_notification_info)
    elif current_user.type == "operator":
        for notification in notifications:
            info = {"timestamp": notification['timestamp'],
                    "contagion_datetime": notification['contagion_datetime']}
            is_future = notification['timestamp'] < notification['contagion_datetime']
            info['is_future'] = is_future
            if is_future:
                customer_phone_number = UserManager.get_user_by_id(notification.positive_customer_id).phone
                info['customer_phone_number'] = customer_phone_number
            processed_notification_info.append(info)
        return render_template('operator_notifications.html', current_user=current_user,
                               notifications=processed_notification_info)
