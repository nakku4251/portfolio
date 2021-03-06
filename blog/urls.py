from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path("detail/<int:pk>", views.PostDetail.as_view(), name="post_detail"),
    path("comment/<int:pk>/", views.CommentCreate.as_view(), name="comment_create"),
    path("category/<int:pk>/", views.PostCategoryList.as_view(), name="post_category_list"),
    path("tag/<int:pk>/", views.PostTagList.as_view(), name="post_tag_list"),
    path("create/", views.PostCreate.as_view(), name="post_create"),
    path("tag_create/", views.TagCreate.as_view(), name="tag_create"),
    path("category_create", views.CategoryCreate.as_view(), name="category_create"),
    path("update<int:pk>/", views.PostUpdate.as_view(), name="post_update"),
    path("delete<int:pk>/", views.PostDelete.as_view(), name="post_delete"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('index/', views.IndexView.as_view(), name="index"),
    path('create_account/', views.UserCreateView.as_view(),name="create"),
]
