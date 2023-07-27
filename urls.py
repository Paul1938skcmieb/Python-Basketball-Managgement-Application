from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    # Login/Register
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('registerplayer/', views.register_player, name='register-player'),
    path('registercoach/', views.register_coach, name='register-coach'),

    # Activate
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    # Calendar
    path('index/', views.index, name='index'),
    path('index/all_events/', views.all_events, name='all_events'),
    path('index/add_event/', views.add_event, name='add_event'),
    path('index/update/', views.update, name='update'),
    path('index/remove/<int:event_id>/', views.remove, name='remove'),

    # Home
    path('', views.home, name='home'),

    # Player stats, table, CRUD
    path('playerstats/', views.playerstats, name='playerstats'),
    path('playerstats/addplayer/', views.addPlayer, name='addplayer'),
    path('playerstats/updateplayer/<str:pk>/',
         views.updatePlayer, name='updatePlayer'),
    path('playerstats/deleteplayer/<str:pk>/',
         views.deletePlayer, name='delete-player'),
    path('playerstats/playerprofile/<str:pk>/',
         views.playerProfile, name='player-profile'),

    # Coach CRUD
    path('coachtable/', views.displaycoaches, name='displaycoaches'),
    path('coachtable/updatecoach/<str:pk>/',
         views.updateCoach, name='update-coach'),
    path('coachtable/deletecoach/<str:pk>/',
         views.deleteCoach, name='delete-coach'),
    path('coachtable/coachprofile/<str:pk>/',
         views.coachProfile, name='coach-profile'),

    # Visuals
    path('playerstats/visuals/', views.visuals, name='visuals'),

    # Draw
    path('draw/', views.draw, name='draw'),
    path('save-drawing/', views.save_drawing, name='save_drawing'),
    path('view-drawing/', views.view_drawing, name='view_drawing'),

    # Payment
    path('payment/', views.make_payment, name='payment'),
    path('financialinfo/', views.displayPayments, name='financial-info')


]
