import os

from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import prod_bp
from app.models import Product, Category
from app.forms import ProductForm
from ... import db


@prod_bp.route('/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    # Fetch the product details using the product_id
    product = Product.query.get_or_404(product_id)
    return render_template('app/product_detail.html', product=product)

@login_required
@prod_bp.route('/edit/<int:pk>', methods=['GET', 'POST'])
def product_edit(pk):
    product = Product.query.filter_by(id=pk, seller=current_user).first_or_404()
    if request.method == "POST":
        form = ProductForm(request.form)
        if form.validate_on_submit():
            product.title = form.title.data
            product.description = form.description.data
            product.price = form.price.data
            product.location = form.location.data
            product.image = form.image.data
            new_category_name = request.form.get("new_category")
            if new_category_name:
                new_category = Category()
                new_category.name = new_category_name
                product.category = new_category
            else:
                selected_category = request.form.get("category")
                if selected_category:
                    product.category = Category.query.get(selected_category)
            product.seller = current_user
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('main.home'))
        if form.errors:
            print(form.errors.values())

    else:
        form = ProductForm(obj=product)

    categories = Category.query.all()
    return render_template('app/product_edit.html', form=form, product=product, categories=categories)


@prod_bp.route('/create', methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product()
        product.title = form.title.data
        product.description = form.description.data
        product.price = form.price.data
        product.location = form.location.data
        product.seller = current_user

        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static', 'media/product_images', filename)
            image_file.save(image_path)
            product.image = f'media/product_images/{filename}'

        new_category_name = request.form.get("new_category")
        if new_category_name:
            new_category = Category(name=new_category_name)
            db.session.add(new_category)
            db.session.flush()  # To generate the ID of the new category
            product.category = new_category
        else:
            selected_category = request.form.get("category")
            if selected_category:
                product.category_id = selected_category

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('app/product_form.html', form=form, categories=Category.query.all())


@login_required
@prod_bp.route('/delete/<int:pk>', methods=['POST'])  # POST method for deletion
def delete(pk):
    # Get product by primary key and seller
    product = Product.query.filter_by(id=pk, seller=current_user).first_or_404()

    db.session.delete(product)  # Delete the product from the session
    db.session.commit()  # Commit the deletion to the database

    flash('Product deleted successfully!', 'success')  # Flash a success message
    return redirect(url_for('prof.profile'))  # Redirect to the profile
