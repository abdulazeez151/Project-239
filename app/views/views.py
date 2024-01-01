from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.models.products import Products
from app.models.address import Address
from app.models.users import Users
from app.models.orders import Orders
from app.models.tickets import Tickets
from app import db

from flask_cors import cross_origin

views = Blueprint('views', __name__, url_prefix="/")

@views.route('/')
@cross_origin()
# Route handler for rendering the login page
def login():
    try:
        return render_template("/login/login.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route('/dashboard')
@cross_origin()
# Route handler for the dashboard page
def dashboard():
    try:
        # Used to query all products
        products = Products.query.all()
        return render_template("/dashboard/dashboard.html", products=products, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route('/profile')
@cross_origin()
# Route handler for the user profile page
def profile():
    try:
        # Used to query a user by ID
        user_id = request.args.get("id")
        user = Users.query.filter_by(id=user_id).first()
        
        # Used to join tables (products and orders)
        order_query = f"select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id;"
        orders = db.engine.execute(order_query).all()

        # Queries for related entities (tickets and addresses)
        ticket_query = f"select * from tickets where user_id='{user['id']}';"
        tickets = db.engine.execute(ticket_query).all()
        address_query = f"select * from address where user_id='{user['id']}'"
        addresses = db.engine.execute(address_query).all()

        return render_template("/profile/profile.html", user=user, orders=orders, addresses=addresses, tickets=tickets, user_id=session.get("user_id"))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route('/order')
@cross_origin()
# Route handler for the customer order page
def order():
    try:
        product_id = request.args.get("id")
        if not product_id:
            return jsonify({
                "message": "No product for purchase!",
                "status": "error"
            }), 400
        # SQL query is used to fetch a product by ID
        query = f"select * from products where id={product_id};"
        product = db.engine.execute(query).first()
        
        # SQL query to fetch addresses
        address_query = f"select * from address where user_id='{session.get('user_id')}'"
        addresses = db.engine.execute(address_query).all() or []

        return render_template("/order/order.html", product=product, addresses=addresses, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route("/help")
@cross_origin()
# Route handler for the help page (In case the user needs any help)
def help_page():
    try:
        return render_template("/help/help.html", user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route("/editor")
@cross_origin()
# Route handler for the editor page
def editor():
    try:
        return render_template("/editor/editor.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400
