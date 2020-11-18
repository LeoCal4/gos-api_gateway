import requests
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

auth = Blueprint('auth', __name__)
RESTA_MS_URL = app.config['RESTA_MS_URL']
USERS_ENDPOINT = app.config['USERS_MS_URL']

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
                return redirect(url_for('auth.operator', id=user.id))
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
        # reservations = ReservationManager.retrieve_by_customer_id(id)

        return render_template('customer_profile.html',
                               # reservations=reservations, restaurants=restaurants,
                               form=form, social_form=social_form)

    return redirect(url_for('home.index'))


@auth.route('/operator/<int:op_id>', methods=['GET', 'POST'])
def operator(op_id):
    """This method allows the operator to access the page of its personal info

    Args:
        id (int): univocal identifier of the operator

    Returns:
        Redirects the view to personal page of the operator
    """
    filter_form = FilterForm()

    url = "%s/restaurants/details/%s" % (RESTA_MS_URL, op_id)
    res = requests.get(url)
    json_data = res.json()
    if res.status_code != 200:
        print(json_data['message'])
        restaurant = None
    else:
        restaurant = json_data['details']['restaurant']
    return render_template('operator_profile.html',
                    restaurant=restaurant, filter_form=filter_form)


@auth.route('/authority/<int:id>/<int:positive_id>', methods=['GET', 'POST'])
def authority(id, positive_id):
    """This method allows the Health Authority to see its personal page.

    Args:
        id (int): the univocal identifier for the Health Authority
        positive_id (int): the identifier of the positive user

    Returns:
        Redirects to the page of the Health Authority
    """
    if current_user.id == id:
        authority = AuthorityManager.retrieve_by_id(id)
        ha_form = AuthorityForm()
        pos_customers = CustomerManager.retrieve_all_positive()
        search_customer = CustomerManager.retrieve_by_id(positive_id)
        return render_template('authority_profile.html', current_user=authority,
                               form=ha_form, pos_customers=pos_customers,
                               search_customer=search_customer)
    return redirect(url_for('home.index'))


@auth.route('/logout')
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
    notifications = NotificationManager.retrieve_by_target_user_id(current_user.id)
    processed_notification_info = []
    if current_user.type == "customer":
        for notification in notifications:
            restaurant_name = RestaurantManager.retrieve_by_id(notification.contagion_restaurant_id).name
            processed_notification_info.append({"timestamp": notification.timestamp,
                                                "contagion_datetime": notification.contagion_datetime,
                                                "contagion_restaurant_name": restaurant_name})
        return render_template('customer_notifications.html', current_user=current_user,
                               notifications=processed_notification_info)
    elif current_user.type == "operator":
        for notification in notifications:
            info = {"timestamp": notification.timestamp,
                    "contagion_datetime": notification.contagion_datetime}
            is_future = notification.timestamp < notification.contagion_datetime
            info['is_future'] = is_future
            if is_future:
                customer_phone_number = UserManager.retrieve_by_id(notification.positive_customer_id).phone
                info['customer_phone_number'] = customer_phone_number
            processed_notification_info.append(info)
        return render_template('operator_notifications.html', current_user=current_user,
                               notifications=processed_notification_info)
