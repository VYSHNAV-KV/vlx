from django.urls import path
from webapp import views
from django.urls import path


urlpatterns=[
    path('', views.home1, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('search/', views.search_products, name='search_products'),
    path('add_dataform/',views.add_dataform,name='add_dataform'),
    path('save_dataform/', views.save_dataform, name='save_dataform'),
    path('edit_dataform/<int:pro_id>/', views.edit_dataform, name='edit_dataform'),
    path('update_dataform/<int:pro_id>/', views.update_dataform, name='update_dataform'),
    path('delete_dataform/<int:pro_id>/', views.delete_dataform, name='delete_dataform'),

    path('verthe/', views.verthe, name='verthe'),
    path('fetch_subcategories/', views.fetch_subcategories, name='fetch_subcategories'),

    path('signup_page', views.signup_page, name='signup_page'),
    path('signin_page', views.signin_page, name='signin_page'),
    path('save_signup/', views.save_signup, name='save_signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),

    path('myitem/', views.myitem, name='myitem'),

    path('home3/', views.home3, name='home3'),
    path('subcategory/<cat_name>/', views.subcategory, name='subcategory'),
    path('product_page/<str:subcat_name>/', views.product_page, name='product_page'),
    path('product_single/<int:pro_id>/', views.product_single, name='product_single'),
    # path('message_page/', views.message_page, name='message_page'),
    # path('message/<int:product_id>/', views.message_interface, name='message'),
    # path('product/<int:product_id>/',views.product_detail, name='product'),
    # path('product/<int:product_id>/messages/', message_history, name='message_history'),
    #
    # Path for sending a message (form submission)
    # path('product/<int:product_id>/message/', views.send_message, name='send_message'),

    # Path for viewing message history
    # path('product/<int:product_id>/messages/', views.message_view, name='message_view'),

    path('product/<int:product_id>/messages/', views.message_view, name='message_view'),
    path('product/<int:product_id>/send_message/', views.send_message, name='send_message'),

    # path('cart/', views.cart, name='cart'),
    path('save_cart/', views.save_cart, name='save_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),


    path('submit_ad/', views.submit_ad, name='submit_ad'),

    path('contact/', views.contact, name='contact'),
    path('save_page/', views.save_page, name='save_page'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('like/<int:product_id>/', views.like_product, name='like_product')
    # path('payment/', views.payment, name='payment'),








]