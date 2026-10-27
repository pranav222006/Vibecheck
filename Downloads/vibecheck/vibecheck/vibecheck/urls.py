from django.urls import include, path
urlpatterns = [path("", include("myapp.urls"))]
handler404 = "myapp.views.custom_404"
handler500 = "myapp.views.custom_500"
