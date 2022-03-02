from django.contrib import admin
from django.urls import include, path
from polls import views
from polls.views import ReceiveImages
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('',views.home,name="add_new" ),
    path('prediction', ReceiveImages.as_view(),name="file_receive"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
