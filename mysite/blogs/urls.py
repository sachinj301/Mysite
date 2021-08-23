from django.conf.urls import url
from django.urls import path
from blogs import views
from .feeds import LatestPostsFeed



app_name = 'blogs'
# urlpatterns=[
#     path('',views.post_list,name='post_list'),
#     #url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
#      #   r'(?P<post>[-\w]+)/$',views.post_detail,name="post_detail"),
#     path('<int:post_id>/share/',views.post_share, name='post_share'),
#     path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),

#]
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
   # path('tag/<slug:tag_slug>/',
    #     views.post_list, name='post_list_by_tag'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name="post_feed"),
]
