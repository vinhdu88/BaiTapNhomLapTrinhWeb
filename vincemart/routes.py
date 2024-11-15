from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, session
from vincemart import app, db
from vincemart.forms import RegisterForm, LoginForm
from vincemart.models import Users, Products, Specifications
from flask_login import login_user, logout_user, current_user
import math


@app.route('/')
@app.route('/home')
def home():
    products1 = Products.query.order_by(Products.rating.desc()).limit(4).all()
    featured_products = present_products(products1)
    products2 = Products.query.order_by(Products.date_added.desc()).limit(4).all()
    latest_products = present_products(products2)
    return render_template('home.html', featured_products = featured_products, latest_products = latest_products)


@app.route('/products', methods = ['GET', 'POST'])
def products():
    products = Products.query.all()
    default_option = present_products(products)
    products1 = Products.query.order_by(Products.price.desc()).all()
    price = present_products(products1)
    products2 = Products.query.order_by(Products.rating.desc()).all()
    rating = present_products(products2)
    products3 = Products.query.order_by(Products.quantity.desc()).all()
    quantity = present_products(products3)
    return render_template('products.html', searched_products = searched_products,default_option = default_option, price = price, rating = rating, quantity = quantity)

@app.route('/searched_products', methods = ['GET', 'POST'])
def searched_products():
    if request.method == 'POST':
        search = request.form.get('search')
        products0 = Products.query.filter(Products.product_name.like(f'%{search}%') | Products.brand.like(f'%{search}%')).all()
        searched_products = present_products(products0)

    return render_template('searched_products.html', searched_products = searched_products)

@app.route('/account', methods = ['GET', 'POST'])
def account():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        user_to_create = Users(username = register_form.username.data,
                               email = register_form.email_address.data,
                               address = register_form.address.data,
                               phone = register_form.phone.data,
                               password = register_form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account created successfully! Now login to get started', category='success')
        return redirect(url_for('account'))
    
    if register_form.errors != {}:
        for err_msg in register_form.errors.values():
            flash(err_msg, category='error')

        
    if login_form.validate_on_submit():
        attempted_user = Users.query.filter_by(username = login_form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(login_form.password.data):
            login_user(attempted_user)
            for _ in get_flashed_messages():
                pass
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            
            return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='error') 

    return render_template('account.html', register_form = register_form, login_form = login_form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', category='success')
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    current_cart = []
    current_subtotal = 0
    if 'cart' in session: 
        current_cart = session.get('cart', [])
        for item in current_cart:
            current_subtotal += item['subtotal']
    return render_template('cart.html', carts = current_cart, subtotalP = current_subtotal)

@app.route('/checkout')
def checkout():
    if 'cart' in session:
        current_cart = session.get('cart', [])
        present_cart_items = ''
        current_subtotal = 0
        current_quantity = 0
        for item in current_cart:
            current_quantity += item['quantity']
            current_subtotal += int(item['subtotal'])
        present_cart_items = present_cart_item(current_cart)
    return render_template('checkout.html', present_cart_items = present_cart_items, subtotalP = current_subtotal, current_quantity = current_quantity)

@app.route('/proceed_checkout', methods=['GET', 'POST'])
def proceed_checkout():
    if request.method == 'POST':
        subtotal = request.form.get('subtotal')
        user = Users.query.filter_by(username = current_user.username).first()
        if user.budget >= int(subtotal) and 'cart' in session:
            user.budget = user.budget - int(subtotal)
            current_cart = session.get('cart', [])
            for item in current_cart:
                product = Products.query.filter_by(product_id = item['product_id']).first()
                product.quantity = product.quantity - item['quantity']
                db.session.commit()
            session.pop('cart', None)
            flash('Checkout successfully!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Insufficient budget!', category='error')
            return redirect(url_for('home'))
        
@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    product = Products.query.filter_by(product_id = product_id).first()
    relate_products = Products.query.filter_by(brand = product.brand).limit(4).all()
    related_products = present_products(relate_products)
    return render_template('product_details.html', product = product, related_products = related_products)

@app.route('/add_to_cart', methods = ['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Products.query.filter_by(product_id = product_id).first()
        product_dict = {'product_id': product.product_id, 'product_name': product.product_name, 'price': product.price, 'image': product.product_image, 'quantity': quantity, 'subtotal': product.price * quantity}
        cart = session.get('cart', [])
        found = False
        for item in cart:            
            if item['product_id'] == int(product_id):
                item['quantity'] = int(item['quantity']) + int(quantity)
                found = True
                break
        if not found:
            cart.append(product_dict)
        for item in cart: 
            item['subtotal'] = int(item['price']) * int(item['quantity'])
        session['cart'] = cart
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('product_details', product_id = product_id))

@app.route('/update_cart', methods=['GET', 'POST'])
def update_cart():
    cart = session.get('cart', [])
    new_cart = []
    for product in cart:
        product_id = str(product['product_id'])
        if f'quantity-{product_id}' in request.form:
            quantity = int(request.form[f'quantity-{product_id}'])
            if quantity == 0 in request.form:
                continue
            product['quantity'] = quantity
            product['subtotal'] = int(product['price']) * int(product['quantity'])
        new_cart.append(product)
    session['cart'] = new_cart
    return redirect(url_for('cart'))


@app.route('/remove_item_from_cart/<int:product_id>')
def remove_item_from_cart(product_id):
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            cart.remove(item)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/comparison/<int:product_id>')
def comparison(product_id):
    product1_result  = Products.query.filter_by(product_id = product_id).first()
    product1_specs = Specifications.query.filter_by(product_id = product_id).first()
    return render_template('comparison.html', product1_specs = product1_specs, product1_result = product1_result)

@app.route('/comparison/search_product/<int:product_id>', methods = ['GET', 'POST'])
def search_product(product_id):
    if request.method == 'POST':
        product1_result  = Products.query.filter_by(product_id = product_id).first()
        product1_specs = Specifications.query.filter_by(product_id = product_id).first()
        product2 = request.form.get('product2')
        product2_result = Products.query.filter(Products.product_name.like(f'%{product2}%')).first()
        product2_specs = Specifications.query.filter(Specifications.product_id == product2_result.product_id).first()
        return render_template('comparison.html', product2_specs = product2_specs, product2_result = product2_result, product1_specs = product1_specs, product1_result = product1_result)
    return render_template('comparison.html', product1_specs = product1_specs, product1_result = product1_result)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
def present_products(products):
    count = 0
    html = ''
    for product in products:
        stars = rating(product.rating)
        if count % 4 == 0:
            html += '<div class="row">'
        product_image_path = url_for('static', filename=f'products/{product.product_image}', _external=True)
        html += f'<a href="/product_details/{product.product_id}"><div class="col-4"><div class="image-wrapper"><img src="{product_image_path}" alt="{product.product_name}"></div> <h4>{product.product_name}</h4><div class="rating">{stars}</div><p>{product.price}$</p><p>In stock: <b>{product.quantity}</b></p></div></a>'
        count += 1
        if count % 4 == 0 or count == len(products):
            html += '</div>'
    return html
def rating(product_rating):
    rating = round(product_rating * 2) / 2
    rating_string = ''
    
    for i in range(math.floor(rating)):
        rating_string += '<i class="fa-solid fa-star"></i>'
    
    if rating % 1 != 0.0:
        rating_string += '<i class="fa-regular fa-star-half-stroke"></i>'
    
    for i in range(math.ceil(rating), 5):
        rating_string += '<i class="fa-regular fa-star"></i>'
    return rating_string


def present_cart_item(cart):
    html = ''
    for item in cart:
        product_image_path = url_for('static', filename=f'products/{item["image"]}', _external=True)
        html += f'<div class="item"> <div class="img"><img src="{product_image_path}"></div> <div class="info"> <div class="name">{item["product_name"]}</div> <div class="price">${item["price"]}/1 product</div> </div> <div class="quantity">{item["quantity"]}</div> <div class="returnPrice">${item["subtotal"]}</div> </div>'
    return html