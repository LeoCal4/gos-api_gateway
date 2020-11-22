from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from gooutsafe.forms.authority import AuthorityForm
from gooutsafe.rao.user_manager import UserManager
from gooutsafe.rao.notification_tracing_manager import NotificationTracingManager as ntm
from gooutsafe.rao.restaurant_manager import RestaurantManager
from gooutsafe.rao.reservation_manager import ReservationManager

authority = Blueprint('authority', __name__)


@authority.route('/ha/search_customer', methods=['POST'])
@login_required
def search_customer():
    """Method that the health authority uses to search through the users.

    Returns:
        Redirects the view to the home page of the health authority.
        If this method is accessed by an unathorized user, it redirects the
        view to the index page
    """
    if current_user is not None and current_user.type == 'authority':
        form = AuthorityForm()
        customer = None
        if request.method == 'POST':
            track_type = form.data['track_type']
            customer_ident = form.data['customer_ident']
            if track_type == 'SSN':
                customer = UserManager.get_user_by_social_number(customer_ident)
            elif track_type == 'Email':
                customer = UserManager.get_user_by_email(customer_ident)
            else:
                customer = UserManager.get_user_by_phone(customer_ident)
            if customer is None:
                flash("The customer doesn't exist")
                return redirect(url_for('auth.authority', id=current_user.id, positive_id=0))
        return redirect(url_for('auth.authority', id=current_user.id, positive_id=customer.id))
    else:
        return redirect(url_for('home.index'))


@authority.route('/ha/mark_positive/<int:customer_id>', methods=['POST'])
@login_required
def mark_positive(customer_id):
    """Through this method the health authority can set the health status
    of a specific user to "positive".

    Args:
        customer_id ([int]): univocal id of the user

    Returns:
        Redirects the view to the health authority's home page
    """
    if current_user is not None and current_user.type == 'authority':
        if request.method == 'POST':
            customer = UserManager.get_user_by_id(customer_id)
            if customer is not None and customer.health_status:
                flash("Customer is already set to positive!")
            #TODO set health status for customer
            elif customer is not None:
                response = UserManager.update_health_status(customer.id)
                if response.status_code == 200:
                    flash("Customer set to positive!")
                    ntm.trigger_contact_tracing(positive_id=customer.id) 
                else:
                    flash("Error during the operation")
                #we have to do this in user microservice
                #schedule_revert_customer_health_status(customer.id)
    return redirect(url_for('auth.authority', id=current_user.id, positive_id=0))


@authority.route('/ha/contact/<int:contact_id>', methods=['GET'])
@login_required
def contact_tracing(contact_id):
    """This method allows the health authority to retrieve the list of
    contacts, given a positive user

    Args:
        contact_id (id): univocal id of the user

    Returns:
        Redirects the view to the health authority's home page
    """
    if current_user is not None and current_user.type == 'authority':
        customer = UserManager.get_user_by_id(user_id=contact_id)
        if customer is not None:
            tracing_list = ntm.get_contact_tracing_list(customer_id=customer.id)
            cust_contacts = []
            restaurant_contacts = []
            date_contacts = []
            for res in tracing_list:
                customer = UserManager.get_user_by_id(res['contact_id'])
                cust_contacts.append(customer)
                restaurant = RestaurantManager.get_restaurant_sheet(restaurant_id=res['restaurant_id'])
                restaurant_contacts.append(restaurant['restaurant']['name'])
                reservation = ReservationManager.get_reservation(reservation_id=res['reservation_id'])
                date_contacts.append(reservation['start_time'])
            return render_template('contact_tracing_positive.html', customer=customer, pos_contact=cust_contacts,
                                   res_contact=restaurant_contacts, date_contact=date_contacts)
        else:
            return redirect(url_for('auth.authority', id=current_user.id, positive_id=0))
    else:
        return redirect(url_for('home.index'))
