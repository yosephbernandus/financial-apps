from django.conf.urls import include
from django.urls import path

app_name = "api"

urlpatterns = [
    path('auth/', include('financial_server.api.auth.urls', namespace='auth')),
    path('profile/', include('financial_server.api.profile.urls', namespace='profile')),
    path('categories/', include('financial_server.api.categories.urls', namespace='categories')),
    path('goals/', include('financial_server.api.goals.urls', namespace='goals')),
    path('transactions/', include('financial_server.api.transactions.urls', namespace='transactions')),
]
