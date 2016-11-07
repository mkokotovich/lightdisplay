from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^imageframe/', TemplateView.as_view(template_name="videofeed/imageframe.html"), name='imageframe'),
    url(r'^$', views.index, name='index'),
]
