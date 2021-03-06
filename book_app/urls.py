from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "book_app"

urlpatterns = [
	url(r"^login/$", 
			auth_views.LoginView.as_view(
				template_name="book_app/login.html",
			),
			name='login'),
    url(r"^logout/$", auth_views.LogoutView.as_view(
    		template_name="book_app/index.html"
    	), name="logout"),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^book_table/(?P<pk>\d+)/$', views.BookTableView.as_view(), name='book_table'),
    url(r'^upload/$', views.UploadBookDataView.as_view(), name='upload'),
    url(r'^csv_list/$', views.CSVBookListView.as_view(), name='csv_list')
]