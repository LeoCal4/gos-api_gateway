from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import (logout_user, login_user, login_required)
import requests

from flask_login import current_user
from gooutsafe.forms import LoginForm
from gooutsafe.forms.authority import AuthorityForm
from gooutsafe.forms.filter_form import FilterForm
from gooutsafe.forms.reservation import ReservationForm
from gooutsafe.forms.update_customer import AddSocialNumberForm


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
        response = requests.post("http://127.0.0.1:5001/login", 
                            json={'email': email, 'password':password})

        user = response.json()
        if response.status_code != 200:
            flash('The user does not exist!')
            return render_template('login.html', form=form, re_login=re)
        
        if user["type"] == 'operator':
            return redirect('/operator/%d' % user["user_id"])
        elif user["type"] == 'customer':
            return redirect('/profile/%d' % user["user_id"])
        else:
            return redirect('/authority/%d/0' % user["user_id"])

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

    """ if current_user.id == id:
        reservations = ReservationManager.retrieve_by_customer_id(id)
        form = ReservationForm()
        social_form = AddSocialNumberForm()
        customer = CustomerManager.retrieve_by_id(id)
        restaurants = RestaurantManager.retrieve_all()
        return render_template('customer_profile.html', customer=customer,
                               reservations=reservations, restaurants=restaurants, 
                               form=form, social_form=social_form)"""

    return redirect(url_for('home.index'))


@auth.route('/operator/<int:id>', methods=['GET', 'POST'])
def operator(id):
    """This method allows the operator to access the page of its personal info

    Args:
        id (int): univocal identifier of the operator

    Returns:
        Redirects the view to personal page of the operator
    """
    """
    filter_form = FilterForm()
    restaurant = Restaurant.query.filter_by(owner_id=id).first()
    return render_template('operator_profile.html',
                    restaurant=restaurant, filter_form=filter_form)"""

    return redirect(url_for('home.index'))



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
    return redirect('/')


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
        return render_template('customer_notifications.html', current_user=current_user, notifications=processed_notification_info)
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
        return render_template('operator_notifications.html', current_user=current_user, notifications=processed_notification_info)
