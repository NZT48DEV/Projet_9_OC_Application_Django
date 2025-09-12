from django.contrib import admin
from reviews.models import Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'note', 'commentary', 'author', 'date_created')


admin.site.register(Review, ReviewAdmin)

