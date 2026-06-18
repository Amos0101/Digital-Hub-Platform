from django.urls import path
from . import views

urlpatterns = [
    # public
    path('', views.landing_page, name='landing'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),

    # dashboard auth
    path('dashboard/login/',  views.dashboard_login,  name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),

    # dashboard pages
    path('dashboard/',  views.dashboard_home, name='dashboard_home'),
    path('dashboard/events/',views.dashboard_events, name='dashboard_events'),
    path('dashboard/events/create/', views.dashboard_event_create,          name='dashboard_event_create'),
    path('dashboard/events/<int:pk>/edit/',               views.dashboard_event_edit,            name='dashboard_event_edit'),
    path('dashboard/events/<int:pk>/delete/',             views.dashboard_event_delete,          name='dashboard_event_delete'),
    path('dashboard/announcements/',                      views.dashboard_announcements,         name='dashboard_announcements'),
    path('dashboard/announcements/create/',               views.dashboard_announcement_create,   name='dashboard_announcement_create'),
    path('dashboard/announcements/<int:pk>/edit/',        views.dashboard_announcement_edit,     name='dashboard_announcement_edit'),
    path('dashboard/announcements/<int:pk>/delete/',      views.dashboard_announcement_delete,   name='dashboard_announcement_delete'),
    path('dashboard/registrations/',                      views.dashboard_registrations,         name='dashboard_registrations'),
# Speakers
    path('dashboard/speakers/',                     views.dashboard_speakers,        name='dashboard_speakers'),
    path('dashboard/speakers/create/',               views.dashboard_speaker_create,  name='dashboard_speaker_create'),
    path('dashboard/speakers/<int:pk>/edit/',        views.dashboard_speaker_edit,    name='dashboard_speaker_edit'),
    path('dashboard/speakers/<int:pk>/delete/',      views.dashboard_speaker_delete,  name='dashboard_speaker_delete'),

    # Sponsors
    path('dashboard/sponsors/',                      views.dashboard_sponsors,        name='dashboard_sponsors'),
    path('dashboard/sponsors/create/',                views.dashboard_sponsor_create,  name='dashboard_sponsor_create'),
    path('dashboard/sponsors/<int:pk>/edit/',         views.dashboard_sponsor_edit,    name='dashboard_sponsor_edit'),
    path('dashboard/sponsors/<int:pk>/delete/',       views.dashboard_sponsor_delete,  name='dashboard_sponsor_delete'),

    # Schedule
    path('dashboard/schedule/',                       views.dashboard_schedule,        name='dashboard_schedule'),
    path('dashboard/schedule/create/',                views.dashboard_schedule_create, name='dashboard_schedule_create'),
    path('dashboard/schedule/<int:pk>/edit/',         views.dashboard_schedule_edit,   name='dashboard_schedule_edit'),
    path('dashboard/schedule/<int:pk>/delete/',       views.dashboard_schedule_delete, name='dashboard_schedule_delete'),
path('dashboard/schedule/bulk/', views.dashboard_schedule_bulk, name='dashboard_schedule_bulk'),
]