from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import (login_user, login_required, current_user)

from gooutsafe.forms import UserForm, LoginForm
from gooutsafe.forms.update_customer import UpdateCustomerForm, AddSocialNumberForm
from gooutsafe.auth.user import User
import requests

users = Blueprint('users', __name__)


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
            url = "http://127.0.0.1:5001/operator"
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
            url = "http://127.0.0.1:5001/customer"
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
            flash("User already present in the database")
            return render_template('create_user.html', form=form, user_type=type_)
    else:
        for fieldName, errorMessages in form.errors.items():
            for errorMessage in errorMessages:
                flash('The field %s is incorrect: %s' % (fieldName, errorMessage))

    return render_template('create_user.html', form=form, user_type=type_)


@users.route('/delete_user/<int:id_>', methods=['GET', 'POST'])
@login_required
def delete_user(id_):
    """Deletes the data of the user from the database.

    Args:
        id_ (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """
    if current_user.id == id_:
        user = UserManager.retrieve_by_id(id_)
        if user is not None and user.type == "operator":
            restaurant = RestaurantManager.retrieve_by_operator_id(id_)
            if restaurant is not None:
                RestaurantManager.delete_restaurant(restaurant)
        
        UserManager.delete_user_by_id(id_)
    return redirect(url_for('home.index'))


@users.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    """This method allows the user to edit their personal information.

    Args:
        id (int): the univocal id for the user

    Returns:
        Redirects the view to the personal page of the user
    """
    user = UserManager.retrieve_by_id(id)
    if user.type == "customer":        
        form = UpdateCustomerForm()
    elif user.type == "operator":
        form = LoginForm()

    if request.method == "POST":
        if form.is_submitted():
            email = form.data['email']
            searched_user = UserManager.retrieve_by_email(email)
            if searched_user is not None and id != searched_user.id:
                flash("Data already present in the database.")
                return render_template('update_customer.html', form=form)

            password = form.data['password']
            user.set_email(email)
            user.set_password(password)

            if user.type == "customer":
                phone = form.data['phone']
                user.set_phone(phone)
                UserManager.update_user(user)

                return redirect(url_for('auth.profile', id=user.id))

            elif user.type == "operator":
                UserManager.update_user(user)
                return redirect(url_for('auth.operator', id=user.id))

    return render_template('update_customer.html', form=form)


@users.route('/add_social_number/<int:id>', methods=['GET', 'POST'])
@login_required
def add_social_number(id):
    """Allows the user to insert their SSN.

    Args:
        id (int): the univocal id for the user

    Returns:
        Redirects the view to the personal page of the user
    """
    social_form = AddSocialNumberForm()
    user = UserManager.retrieve_by_id(id)
    if request.method == "POST":
        if social_form.is_submitted():
            social_number = social_form.data['social_number']
            user.set_social_number(social_number)
            UserManager.update_user(user)
            
    return redirect(url_for('auth.profile', id=user.id))