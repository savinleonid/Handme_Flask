from flask import render_template, request, session
from app.models import Product, User, Category
from . import main_bp
from sqlalchemy import or_

@main_bp.route('/')
def home():
    # Fetch all categories
    categories = Category.query.all()

    # Fetch all unique locations from products
    locations = {product.location for product in Product.query.all()}

    # Initialize filters
    query = request.args.get('q', session.get('q_filter', ''))
    category_id = request.args.get('category', session.get('category_filter', None))
    location = request.args.get('location', session.get('location_filter', ''))

    # Store filters in session
    session['q_filter'] = query
    session['category_filter'] = category_id
    session['location_filter'] = location

    # Start with all products query
    products_query = Product.query

    # Apply search filter if provided
    if query:
        products_query = products_query.filter(
            or_(
                Product.title.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%'),
                Product.location.ilike(f'%{query}%')
            )
        )

    # Apply category filter if selected
    if category_id:
        try:
            # Convert category_id to an integer
            category_id = int(category_id)
            products_query = products_query.filter_by(category_id=category_id)
        except ValueError:
            # If conversion fails, it means category_id is invalid
            category_id = None

    # Apply location filter if selected
    if location:
        products_query = products_query.filter_by(location=location)

    # Execute the query
    products = products_query.all()

    # Fetch user's profile picture if authenticated
    profile_picture = None
    if '_user_id' in session:  # Assuming user ID is stored in the session
        user = User.query.get(session['_user_id'])  # Adjust based on your user model
        profile_picture = user.profile.profile_picture if user.profile and user.profile.profile_picture else ''

    return render_template('app/home.html',
                           products=products,
                           categories=categories,
                           locations=locations,
                           selected_category=category_id,
                           selected_location=location,
                           profile_picture=profile_picture,
                           query=query)
