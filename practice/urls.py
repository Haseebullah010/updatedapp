from django.contrib import admin
from django.urls import include, path
from polls import views
from polls.views import ReceiveImages

urlpatterns = [
    # path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('',views.home,name="add_new" ),
    path('prediction', ReceiveImages.as_view(),name="file_receive"),
    


]
