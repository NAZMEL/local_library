from django.shortcuts import get_object_or_404, render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # count all objects in table Book
    num_books = Book.objects.all().count()  
    num_instances = BookInstance.objects.all().count()

    # available books where status = 'a'
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    # filter names include 'rr' in Genre
    num_genres = Genre.objects.filter(name__icontains='rr').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context= context)


# class BookDetailView(generic.DetailView):
#     model = Book

# the same BookDetailView
def book_detail_view(request, primary_key):
    # try:
    #     book= Book.objects.get(pk=primary_key)
    # except Book.DoesNotExist:
    #     raise Http404('Book does not exist')

    # the same as previous try-except
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

def author_detail_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    print(author.book)
    return render(request, 'catalog/author_detail.html', context={'author': author})


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context