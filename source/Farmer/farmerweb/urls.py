from django.urls import path
from . import views
app_name="farmerweb"
urlpatterns = [
    path("",views.home,name="index"),
    path("login/",views.index,name="loginpage"),
    path("register/",views.register,name="registerpage"),
    path("dashboard/",views.dashboard,name="dashboardpage"),
    path("cropmanagement/",views.cropmanagement,name="cropmanagementpage"),
    path("diseasecontrol/",views.diseasecontrol,name="diseasepage"),
    path("weatherupdate/",views.weatherupdate,name="weatherpage"),
    path("account/",views.account,name="accountpage"),
    path("logout/",views.user_logout,name="logout"),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('plantation/',views.plantation,name="plantationpage"),
    path('fertilizers/',views.fertilizers,name="fertilizerspage"), 
    path('sellersite/',views.sellersite,name="sellerpage"),
    path('diseasecontrol/<str:diseasename>',views.diseaseshow,name="diseaseshowpage"),
    path('remove_crop/<int:crop_id>', views.remove_crop, name='remove_crop'),
    path('merchantlogin/',views.merchantlogin,name="merchantloginpage"),
    path('merchantregister/',views.merchantregister,name="merchantregisterpage"),
    path('merchantdashboard/',views.merchantdashboard,name="merchanthomepage"),
    path('merchantaccount/',views.merchantaccount,name="merchantaccountpage"),
    path('merchantlogout/',views.merchantlogout,name="merchantlogout"),
    path('schemes/',views.scheme,name="schemes"),
    path("loan/",views.loann,name="loans")
]
