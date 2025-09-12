from django.contrib import admin
from tickets.models import Ticket, Photo

# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'type', 'photo', 'author', 'date_created')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploader', 'date_created')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Photo, PhotoAdmin)
