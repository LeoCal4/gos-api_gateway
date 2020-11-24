import requests
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from gooutsafe import app
from gooutsafe.forms.review import ReviewForm
from gooutsafe.rao.restaurant_manager import RestaurantManager

review = Blueprint('review', __name__)

@review.route('/restaurants/<int:restaurant_id>/review', methods=['GET', 'POST'])
@login_required
def write_review(restaurant_id):
    """This method allows a customer to leave a review in a restaurant that he has been in.
    Only one review is possible.

    Args:
        restaurant_id (int): univocal identifier of the restaurant

    """
    form = ReviewForm()
    if request.method == 'GET':
        bounds = RestaurantManager.get_rating_bounds()
        return render_template('create_review.html', form=form, rating_min_value=bounds['min_value'],
                               rating_max_value=bounds['max_value'])
    if form.is_submitted():
        customer_name = current_user.extra_data.get('firstname') or 'operator' # TODO change
        json_data = {
            'customer_id': current_user.id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'value': form.data['value'],
            'review': form.data['review']
        }
        response, already_written = RestaurantManager.post_review(json_data)
        if response:
            return render_template('thank_you_review.html', already_written=already_written, restaurant_id=restaurant_id)
        else:
            return render_template('thank_you_review.html', restaurant_id=restaurant_id)
