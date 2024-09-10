from django.urls import path
from . import users, products, orders

urlpatterns = [
    path('login/', users.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', users.register, name='register'),
     path('profile/', users.getUserProfile, name="users-profile"),
    path('profile/update/', users.updateUserProfile, name="user-profile-update"),
    path('users/', users.getUsers, name="users"),

    path('user/<str:pk>/', users.getUserById, name='user'),

    path('user/update/<str:pk>/', users.updateUser, name='user-update'),

    path('user/delete/<str:pk>/', users.deleteUser, name='user-delete'),

    path('create-product/', products.createProduct, name='create-product'),
    path('get-products/', products.getProducts, name='get-products'),
    path('product/<str:pk>/', products.getProduct, name="product"),
    path('product/<str:pk>/reviews/', products.createProductReview, name="create-review"),


    path('orders', orders.getOrders, name='orders'),
    path('order_add/', orders.addOrderItems, name='orders-add'),
    path('myorders/', orders.getMyOrders, name='myorders'),

    path('order/<str:pk>/deliver/', orders.updateOrderToDelivered, name='order-delivered'),

    path('order/<str:pk>/', orders.getOrderById, name='user-order'),
    path('order/<str:pk>/pay/', orders.updateOrderToPaid, name='pay'),
]