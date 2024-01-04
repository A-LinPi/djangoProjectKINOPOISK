from django.contrib import admin
from catalog_app.models import *

# Register your models here.
admin.site.register(Genre)
admin.site.register(Country)


@admin.register(Comment)
class adminComment(admin.ModelAdmin):
    list_display = ('user', 'timedata', 'kino', 'active')


@admin.register(ProfileUser)
class adminProfileUser(admin.ModelAdmin):
    list_display = ('user', 'podpiska')


@admin.register(Actor)
class adminActor(admin.ModelAdmin):
    list_display = ('name', 'lastname')
    list_display_links = ('name', 'lastname')


@admin.register(Director)
class adminDirector(admin.ModelAdmin):
    list_display = ('name', 'lastname')
    list_display_links = ('name', 'lastname')


# admin.site.register(Podpiska)


@admin.register(Kino)
class adminKino(admin.ModelAdmin):
    list_display = ('title', 'genre', 'director', 'year', 'country')
    fieldset = (('о фильме', {'fields': ('title', 'genre', 'opisanie')}),
                ('Создатели', {'fields': ('director', 'actors')}),
                ('Остальное', {'fields': ('country', 'year', 'podpiska', 'image')}))

    list_filter = ('genre', 'country', 'podpiska', 'year')


class PodpiskaLine(admin.TabularInline):
    model = Kino


@admin.register(Podpiska)
class adminPod(admin.ModelAdmin):
    inlines = [PodpiskaLine]
