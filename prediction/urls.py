from django.urls  import path
from prediction import views

app_name='prediction'

urlpatterns=[
    path('home/<int:id>',views.Home,name='home'),
    path('',views.Index,name='index'),
    path('mlogin/',views.mLogin,name='mlogin'),
    path('msignup/',views.mSignup,name='msignup'),
    
    path('single/<int:id>',views.Single,name='single'),
    path('logout',views.Logout,name='logout'),
    path('op/<int:id>',views.Op,name='op'),
    path('lab/<int:id>',views.Lab,name='lab'),
    path('contact/',views.Contact,name='contact'),
    path('doc/<int:id>',views.DocPage,name='doc'),
    path('docreg/<int:id>',views.Dreg,name='docreg'),
    path('doclogin/<int:id>',views.Dlogin,name='doclogin'),
    path('ophome/<int:id>',views.OpHome,name='ophome'),
    path('labhome/<int:id>',views.LabHome,name='labhome'),
    path('opedit/<int:id>',views.OpEdit,name='opedit'),
    path('labedit/<int:id>',views.LabEdit,name='labedit'),
    path('dochome/<int:id>',views.DocHome,name='dochome'),
    path('docedit/<int:id>',views.DocEdit,name='docedit'),
    path('printout/<int:id>',views.PrintOut,name='printout'),
    
    

    
]