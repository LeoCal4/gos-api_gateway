import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    """Form created to allow the customers to insert a new review: an integer value
    along with a comment
    """

    value = f.IntegerField(
        'Rate',
        validators=[NumberRange(
            min=0,
            max=10
        )]
    )

    review = f.TextAreaField(
        'Review',
        validators=[DataRequired()]
    )
