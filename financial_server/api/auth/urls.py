from django.urls import path

from .views import AuthLogin, EditPhoto, Register, Logout, ChangePassword, EditProfile, EditPhotoForm

app_name = "auth"

urlpatterns = [
    path('login', AuthLogin.as_view(), name="login"),
    path('register', Register.as_view(), name="register"),
    path('logout', Logout.as_view(), name="logout"),
    path('change-password', ChangePassword.as_view(), name="change_password"),
    path('edit-profile', EditProfile.as_view(), name="edit_profile"),
    path('edit-profile-photo', EditPhoto.as_view(), name="edit_profile_photo"),
]
