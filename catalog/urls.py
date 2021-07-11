from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:primary_key>',views.book_detail_view, name = 'book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.author_detail_view, name = "author-detail"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name = "my-borrowed"),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name = 'all-borrowed'),
    #path('book/<uuid:pk>/renew/', views.renew_book_librarian, name = "renew-book-librarian"),
]