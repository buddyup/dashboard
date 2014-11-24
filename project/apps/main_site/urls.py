from django.conf.urls.defaults import patterns, include, url

from main_site import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^sales-cycle$', views.sales_cycle, name='sales_cycle'),
    url(r'^sales/save$', views.save_sales, name='save_sales'),
    url(r'^intercom$', views.intercom, name='intercom'),
    url(r'^will$', views.will, name='will'),
    url(r'^admin$', views.admin, name='admin'),
)
