from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('voter', views.voter_dashboard, name='voter_dashboard'),
    path('voter/view_election/', views.view_election, name='view_election'),
    path('voter/register-candidate/', views.register_candidate, name='register-candidate'),
    path('voter/candidate-status/', views.candidate_status, name='candidate-status'),
    path('voter/results/', views.results, name='results'),
    path('voter/election-history/', views.election_history, name='election-history'),
    path('voter/rules/', views.rules, name='rules'),
    path('admin1', views.admin_dashboard, name='admin_dashboard'),
    path('admin1/create_elections/', views.create_elections, name='create_elections'),
    path('admin1/manage-elections/', views.manage_elections, name='manage_elections'),
    path('admin1/approve-candidates/', views.approve_candidates, name='approve_candidates'),
    path('admin1/view-results/', views.view_results, name='view_results'),
    path('admin1/voter-logs/', views.voter_logs, name='voter_logs'),
    path('demo',views.demo,name='demo'),
]
