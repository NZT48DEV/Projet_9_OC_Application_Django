from django.contrib import admin
from reviews.models import Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'rating', 'user', 'headline', 'body', 'time_created')


admin.site.register(Review, ReviewAdmin)

