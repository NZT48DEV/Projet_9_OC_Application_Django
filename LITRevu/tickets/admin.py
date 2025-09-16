from django.contrib import admin
from tickets.models import Ticket, Image

# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'type', 'user', 'image', 'time_created')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploader', 'time_created')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Image, ImageAdmin)
