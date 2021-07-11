from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Author, Genre, Book, BookInstance

admin.site.register(Genre)


# Another shape of Admin-panel
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 
                    'last_name',
                    'date_of_birth',
                    'date_of_death')

    fields = ['first_name',
                'last_name', 
                ('date_of_birth', 'date_of_death')]


@admin.register(Book)  # the same: admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    #display all data on admin place
    list_display = ('book', 'imprint', 'due_back')

    #display filter on admin place
    list_filter = ('status', 'due_back')

    # better display edit fields
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )


@admin.register
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'status',
        'borrower',
        'due_back',
        'id',
    )

    list_filter = (
        'status',
        'due_back'
    )

    fieldsets = (
        (None,{
            'fields': (
                'book',
                'imprint',
                'id',
            )
        }),

        ('Availability',{
            'fields': (
                'status',
                'due_back',
                'borrower',
            )
        })
    )

