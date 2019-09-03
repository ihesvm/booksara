from django.contrib import admin

from .models import Book, New, Passwordresetcode, Token


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'picture',
        'is_sold',
        'publisher',
        'date',
        'price',
    )
    list_filter = ('is_sold', 'publisher', 'date')
    search_fields = ('name',)


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'date')
    list_filter = ('date',)


@admin.register(Passwordresetcode)
class PasswordresetcodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'email', 'time', 'username', 'password')
    list_filter = ('time',)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')
    list_filter = ('user',)