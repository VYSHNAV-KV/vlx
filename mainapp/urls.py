from django.urls import path
from mainapp import views
from .views import toggle_approval_mode

urlpatterns=[
    path('index/', views.index, name='index'),
    path('add_category/', views.add_category, name='add_category'),
    path('save_category/', views.save_category, name='save_category'),
    path('display_category/', views.display_category, name='display_category'),
    path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('update_category/<int:cat_id>/', views.update_category, name='update_category'),
    path('delete_category/<int:cat_id>/', views.delete_category, name='delete_category'),

    path('add_product/', views.add_product, name='add_product'),
    path('save_product/', views.save_product, name='save_product'),
    path('display_product/', views.display_product, name='display_product'),
    path('edit_product/<int:pro_id>/', views.edit_product, name='edit_product'),
    path('update_product/<int:pro_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:pro_id>/', views.delete_product, name='delete_product'),

    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('display_subcategory/', views.display_subcategory, name='display_subcategory'),
    path('save_subcategory/', views.save_subcategory, name='save_subcategory'),
    path('edit_subcategory/<int:cat_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('update_subcategory/<int:cat_id>/', views.update_subcategory, name='update_subcategory'),
    path('delete_subcategory/<int:cat_id>/', views.delete_subcategory, name='delete_subcategory'),

    path('login_page/', views.login_page, name='login_page'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    path('display_pending/', views.display_pending, name='display_pending'),
    path('delete_pending/<int:cat_id>/', views.delete_pending, name='delete_pending'),
    path('approve_pending/<int:pk>/', views.approve_pending, name='approve_pending'),
    path('toggle_approval_mode/', views.toggle_approval_mode, name='toggle_approval_mode'),  # URL to render the toggle page
    path('toggle_auto_approval/', views.toggle_auto_approval, name='toggle_auto_approval'),

    path('pending_ads/', views.pending_ads, name='admin_pending_ads'),
    path('approve_ad/<int:ad_id>/', views.approve_ad, name='approve_ad'),
    path('update_rate/', views.update_rate, name='update_rate'),
    path('user_data/', views.user_data, name='user_data'),
    path('delete_data/<int:user_id>/', views.delete_data, name='delete_data'),
    ]
