from flask_restx import Namespace,Resource,fields
from ..models.order import Order
from ..models.user import User
from ..utils import db
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity,jwt_required

order_namespace = Namespace("Order",description="Namespace for order")

order_model = order_namespace.model(
    'Order', {
       'id':fields.Integer(description='Order ID'),
       'quantity':fields.Integer(description='Pizza Quantity',required = True),
       'flavour':fields.String(description='Pizza Flavour',required = True),
       'size': fields.String(description='Pizza Size',required = True,enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']),
       'order_status': fields.String(description='Current Order Status',required = True,enum=['PENDING','IN_TRANSIT','DELIVERED']),
       #'user':fields.Integer(description='User Id',required=True)
    }
)
@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
        Get All Orders
        """
        orders = Order.query.all()

        return orders, HTTPStatus.OK
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Place an order
        """
        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        data = order_namespace.payload
        new_order = Order(
            size = data['size'],
            quantity = data['quantity'],
            flavour = data['flavour'],
        )

        new_order.user = current_user
        new_order.save()
        
        return new_order, HTTPStatus.CREATED

@order_namespace.route('/orders/<int:order_id>')
class GetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self,order_id):
        """
        Get Orders by ID
        """
        order = Order.get_by_id(order_id)

        return order, HTTPStatus.OK
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self,order_id):
        """
        Update an order by ID
        """
        order_update = Order.get_by_id(order_id)
        
        data = order_namespace.payload
        
        order_update.flavour = data["flavour"]
        order_update.quantity = data["quantity"]
        order_update.size = data["size"]

        order_update.update()
        return order_update,HTTPStatus.OK
    
    @jwt_required()
    def delete(self,order_id):
        """
        Delete an order by ID
        """
        order_delete = Order.get_by_id(order_id)

        order_delete.delete()

        return {"message":"Order Delected Successfully"},HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self,user_id,order_id):
        """
        Get a user specific Order 
        """
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
        
        return order,HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self,user_id):
        """
        Get all Orders by a User
        """
        user = User.get_by_id(user_id)

        orders = user.orders

        return orders, HTTPStatus.OK

@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def patch(self,order_id):
        """
        Update an order status
        """
        order_update = Order.get_by_id(order_id)
        
        data = order_namespace.payload

        order_update.order_status = data["order_status"]

        db.session.commit()

        return order_update,HTTPStatus.OK

