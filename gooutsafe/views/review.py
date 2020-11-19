import requests
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from gooutsafe import app
from gooutsafe.forms.review import ReviewForm

review = Blueprint('review', __name__)
RESTA_MS_URL = app.config['RESTA_MS_URL']

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
        res = requests.get('%s/restaurants/rating_bounds' % RESTA_MS_URL)
        bounds = res.json()['bounds']
        return render_template('create_review.html', form=form, rating_min_value=bounds['min_value'],
                               rating_max_value=bounds['max_value'])
    if form.is_submitted():
        json_data = {
            'user_id': current_user.id,
            'restaurant_id': restaurant_id,
            'user_name': current_user.firstname,
            'value': form.data['value'],
            'review': form.data['review']
        }
        res = requests.post('%s/restaurants/review' % RESTA_MS_URL, json=json_data)
        if res.status_code == 201 or res.status_code == 200:
            already_written = res.json()['already_written']
            return render_template('thank_you_review.html', already_written=already_written, restaurant_id=restaurant_id)
        else:
            return render_template('thank_you_review.html', restaurant_id=restaurant_id)
