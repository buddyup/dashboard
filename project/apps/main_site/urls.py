from django.conf.urls.defaults import patterns, include, url

from main_site import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^sales-cycle$', views.sales_cycle, name='sales_cycle'),
    url(r'^sales/save$', views.save_sales, name='save_sales'),
)
