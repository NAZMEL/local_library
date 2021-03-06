from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


def index(request):
    # count visits on the site
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
    print(author)
    return render(request, 'catalog/author_detail.html', context={'author': author})


class BookListView(generic.ListView):
    model = Book
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context
        

# get user's borrowed books 
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')


# get all borrowed books
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception = True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk = pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial = {
            'renewal_date': proposed_renewal_date,
        })

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death'
    ]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = [
        'title',
        'author',
        'summary',
        'isbn',
        'genre'
    ]
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = [
        'title',
        'author',
        'summary',
        'isbn',
        'genre',
    ]
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'