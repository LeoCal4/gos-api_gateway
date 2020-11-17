from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import (login_user, login_required, current_user, logout_user)

from gooutsafe.forms import UserForm, LoginForm
from gooutsafe.forms.update_customer import UpdateCustomerForm, AddSocialNumberForm
from gooutsafe.auth.user import User
import requests
from gooutsafe import app

users = Blueprint('users', __name__)

USERS_ENDPOINT = app.config['USERS_MS_URL']


@users.route('/create_user/<string:type_>', methods=['GET', 'POST'])
def create_user_type(type_):
    """This method allows the creation of a new user into the database

    Args:
        type_ (string): as a parameter takes a string that defines the
        type of the new user

    Returns:
        Redirects the user into his profile page, once he's logged in
    """
    form = LoginForm()
    if type_ == "customer":
        form = UserForm()

    if form.is_submitted():
        email = form.data['email']
        password = form.data['password']
        
        if type_ == "operator":
            url = "%s/operator" % (USERS_ENDPOINT)
            response = requests.post(url, 
                                json={
                                    'type': 'operator',
                                    'email': email, 
                                    'password': password
                                })
        else:
            social_number = form.data['social_number']
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            birthdate = form.data['birthdate']
            date = birthdate.strftime('%Y-%m-%d')
            phone = form.data['phone']
            url = "%s/customer" % (USERS_ENDPOINT)
            response = requests.post(url,
                                json={
                                    'type': 'customer',
                                    'email': email, 
                                    'password': password,
                                    'social_number': social_number,
                                    'firstname': firstname,
                                    'lastname': lastname,
                                    'birthdate': date,
                                    'phone': phone
                                })
        user = response.json()
        if user["status"] == "success":
            to_login = User.build_from_json(user["user"])
            login_user(to_login)
            if to_login.type == "operator":
                return redirect(url_for('auth.operator', id=to_login.id))
            else:
                return redirect(url_for('auth.profile', id=to_login.id))
        else:
            flash("Invalid credentials")
            return render_template('create_user.html', form=form, user_type=type_)
    else:
        for fieldName, errorMessages in form.errors.items():
            for errorMessage in errorMessages:
                flash('The field %s is incorrect: %s' % (fieldName, errorMessage))

    return render_template('create_user.html', form=form, user_type=type_)


@users.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """Deletes the data of the user from the database.

    Args:
        id_ (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """
    logout_user()
    url = "%s/delete/%d" % (USERS_ENDPOINT, id)
    response = requests.get(url)

    if response.status_code != 200:
        flash("Error while deleting the user")
        return redirect(url_for('auth.profile', id=id))
        
    return redirect(url_for('home.index'))


@users.route('/update_customer/<int:id>', methods=['GET', 'POST'])
@login_required
def update_customer(id):
    """This method allows the customer to edit their personal information.

    Args:
        id (int): the univocal id for the customer

    Returns:
        Redirects the view to the personal page of the customer
    """

    url = "%s/user/%d" % (USERS_ENDPOINT, id)
    response = requests.get(url).json()
    user = User.build_from_json(response)

    form = UpdateCustomerForm()
    if form.is_submitted():
        email = form.data['email']
        search_url = "%s/user_email/%s" % (USERS_ENDPOINT, email)
        response = requests.get(url).json()
        searched_user = User.build_from_json(response)
        if searched_user is not None and id != searched_user.id:
            flash("Email already present in the database.")
            return render_template('update_customer.html', form=form)

        password = form.data['password']
        phone = form.data['phone']
        url = "%s/update_customer/%d" % (USERS_ENDPOINT, id)
        response = requests.post(url,
                                json={
                                    'email': email,
                                    'password': password,
                                    'phone': phone
                                })

        if response.status_code != 200:
            flash("Error while updating the user")
        
        return redirect(url_for('auth.profile', id=id))

    return render_template('update_customer.html', form=form)


@users.route('/update_operator/<int:id>', methods=['GET', 'POST'])
@login_required
def update_operator(id):
    """This method allows the operator to edit their personal information.

    Args:
        id (int): the univocal id for the operator

    Returns:
        Redirects the view to the personal page of the operator
    """
    url = "%s/user/%d" % (USERS_ENDPOINT, id)
    response = requests.get(url).json()
    user = User.build_from_json(response)

    form = LoginForm()
    if form.is_submitted():
        email = form.data['email']
        search_url = "%s/user_email/%s" % (USERS_ENDPOINT, email)
        response = requests.get(url).json()
        searched_user = User.build_from_json(response)
        if searched_user is not None and id != searched_user.id:
            flash("Email already present in the database.")
            return render_template('update_customer.html', form=form)
        
        password = form.data['password']
        url = "%s/update_operator/%d" % (USERS_ENDPOINT, id)
        response = requests.post(url,
                                json={
                                    'email': email,
                                    'password': password
                                })
        if response.status_code != 200:
            flash("Error while updating the user")
        
        return redirect(url_for('auth.operator', id=id))

    return render_template('update_customer.html', form=form)


@users.route('/add_social_number/<int:id>', methods=['POST'])
@login_required
def add_social_number(id):
    """Allows the user to insert their SSN.

    Args:
        id (int): the univocal id for the user

    Returns:
        Redirects the view to the personal page of the user
    """

    social_form = AddSocialNumberForm()    
    if social_form.is_submitted():
        social_number = social_form.data['social_number']
        url = "%s/add_social_number/%d" % (USERS_ENDPOINT, id)

        response = requests.post(url,
                            json={
                                'social_number': social_number
                            })

        if response.status_code != 200:
            flash("Error while adding the social number")

    return redirect(url_for('auth.profile', id=id))