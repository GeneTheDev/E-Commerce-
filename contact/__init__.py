from flask import Blueprint, render_template
from forms import ContactForm

contact_bp = Blueprint('contact', __name__, template_folder='templates')


@contact_bp.route('/contact')
def contact_page():
    """Contact page"""
    form = ContactForm()
    if form.validate_on_submit():
        # Handle form submission
        pass
    return render_template("/contact.html", form=form)
