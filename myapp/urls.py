from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('checkout/',views.checkout,name='checkout'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('profile/',views.profile,name='profile'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-product-details/<int:pk>/',views.seller_product_details,name='seller-product-details'),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>/',views.seller_delete_product,name='seller-delete-product'),
    path('seller-view-laptop/',views.seller_view_laptop,name='seller-view-laptop'),
    path('seller-view-camera/',views.seller_view_camera,name='seller-view-camera'),
    path('seller-view-acsessories/',views.seller_view_acsessories,name='seller-view-acsessories'),
    path('product-details/<int:pk>/',views.product_details,name='product-details'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),
    path('change-qty/',views.change_qty,name='change-qty'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),

    # add success and cancel if needed
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('myorder/', views.myorder, name='myorder'),
    path('seller-view-order/',views.seller_view_order,name='seller-view-order'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email')    

   
   ]