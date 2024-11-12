from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .models import Product, Order_Details, Order
from .forms import CheckoutForm
from . import db
from datetime import datetime, timezone

bp = Blueprint('main', __name__)

# This is the home page
@bp.route('/')
def index():
    products = Product.query.all()  
    return render_template('index.html', products=products)

@bp.route('/products')
def products():
    products = Product.query.all()  
    return render_template('products.html', products=products) 

# This is the Product Information Page. It Displays specific fabric information and the user can add things to the cart
@bp.route('/product/<int:product_id>', methods=['GET', 'POST'])  
def product(product_id):  
    product = Product.query.filter(Product.id == product_id).first()
    return render_template('product.html', product = product)

@bp.route('/shopping_cart', methods=['POST','GET'])
def shopping_cart():
    product_id = request.values.get('product_id')
    quantity = request.values.get('quantity')

    # retrieve shopping_cart if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None
    
    # create new order if needed
    if order is None:
        order = Order(customer_name='', customer_email='', total_price=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except Exception as e:
            print(f"Error: {e}")
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for item in order.items:
            totalprice = totalprice + (item.price_per_meter * item.quantity )
    
    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        
        if not any(item.product_id == int(product_id) for item in order.items):
            try:
                print(f"Adding new item")
                order_item = Order_Details()
                order_item.product_id = product.id
                order_item.price_per_meter = product.price_per_meter
                order_item.quantity = quantity
                order.items.append(order_item)
                db.session.commit()
            except Exception as e:
                print(f"Error: {e}")
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.shopping_cart'))
        else:
            try:
                print(f"Adding existing item")
                item.quantity = item.quantity + int(quantity)
                db.session.commit()
            except Exception as e:
                print(f"Error: {e}")
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.shopping_cart'))
    
    return render_template('shopping_cart.html', order = order, totalprice = totalprice)

@bp.route('/delete_item', methods=['POST'])
def delete_item():
    id=request.form['id']
    item = Order_Details.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart successfully')
    return redirect(url_for('main.shopping_cart'))

@bp.route('/clear_cart')
def clear_cart():
    if 'order_id' in session:
        del session['order_id']
        flash('Shopping cart cleared')
    return redirect(url_for('main.index'))  # Redirect to index or any other page after clearing cart

@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if request.method == 'POST':
        if 'order_id' in session:
            order = Order.query.get_or_404(session['order_id'])
        
            if form.validate_on_submit():
                order.customer_name = form.name.data
                order.customer_email = form.email.data
                totalprice = 0
                for item in order.items:
                    totalprice = totalprice + (item.price_per_meter * item.quantity )
                order.total_price = totalprice
                order.order_date = datetime.now()
                try:
                    db.session.commit()
                    del session['order_id']
                    flash('Thank you! One of our awesome team members will contact you soon...')
                    return redirect(url_for('main.index'))
                except Exception as e:
                    print(f"Error: {e}")
                    flash('There was an error completing your order')
            else:
                flash('please enter a valid email address')        
    return render_template('checkout.html', form = form)