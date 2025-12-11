from django.urls import path
from .views import BookmarkListCreateView, RemoveBookmarkView

urlpatterns = [
    path('', BookmarkListCreateView.as_view(), name="bookmarks"),
    path('<int:pk>/', RemoveBookmarkView.as_view(), name="remove-bookmark"),
]
