from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import (login_user, login_required, current_user, logout_user)

from gooutsafe.forms import UserForm, LoginForm
from gooutsafe.forms.update_customer import UpdateCustomerForm, AddSocialNumberForm
from gooutsafe.rao.user_manager import UserManager
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
            response = UserManager.create_operator(
                email,
                password
            )
        else:
            social_number = form.data['social_number']
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            birthdate = form.data['birthdate']
            date = birthdate.strftime('%Y-%m-%d')
            phone = form.data['phone']
            response = UserManager.create_customer(
                'customer',
                email,
                password,
                social_number,
                firstname,
                lastname,
                date,
                phone
            )

        user = response.json()
        if user["status"] == "success":
            to_login = User.build_from_json(user["user"])
            login_user(to_login)
            if to_login.type == "operator":
                return redirect(url_for('auth.operator', op_id=to_login.id))
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

    response = UserManager.delete_user(id)
    if response.status_code != 202:
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

    form = UpdateCustomerForm()
    if form.is_submitted():
        email = form.data['email']
        password = form.data['password']
        phone = form.data['phone']
        searched_user = UserManager.get_user_by_email(email)
        if searched_user is not None and id != searched_user.id:
            flash("Email already present in the database.")
            return render_template('update_customer.html', form=form)

        response = UserManager.update_customer(id, email, password, phone)

        if response.status_code != 204:
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

    form = LoginForm()
    if form.is_submitted():
        email = form.data['email']
        password = form.data['password']
        searched_user = UserManager.get_user_by_email(email)
        if searched_user is not None and id != searched_user.id:
            flash("Email already present in the database.")
            return render_template('update_customer.html', form=form)

        response = UserManager.update_operator(id, email, password)

        if response.status_code != 204:
            flash("Error while updating the user")
        
        return redirect(url_for('auth.operator', op_id=id))

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
        response = UserManager.add_social_number(id, social_number)
        
        if response.status_code != 204:
            flash("Error while updating the user")

    return redirect(url_for('auth.profile', id=id))