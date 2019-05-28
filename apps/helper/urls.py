from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^loggedin$', views.loggedin),
    url(r'^create_new$', views.create_new),
    url(r'^create$', views.create),
    url(r'^desc/(?P<job_id>[0-9]+)$', views.desc),
    url(r'^edit/(?P<job_id>[0-9]+)$', views.edit),
    url(r'^submitedit/(?P<job_id>[0-9]+)$', views.submitedit),
    url(r'^remove/(?P<job_id>[0-9]+)$', views.remove),
    url(r'^giveup/(?P<job_id>[0-9]+)$', views.giveup),
    url(r'^add/(?P<job_id>[0-9]+)$', views.add),
    url(r'^delete$', views.delete)
]
