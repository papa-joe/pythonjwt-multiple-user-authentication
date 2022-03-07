from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, TestView, PeopleLoginView, TestViewp, PeopleLogoutView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('loginp', LoginView.as_view()),
    path('login', PeopleLoginView.as_view()),
    path('user', TestView.as_view()),
    path('people', TestViewp.as_view()),
    path('logout', LogoutView.as_view()),
    path('people_logout', PeopleLogoutView.as_view()),
]