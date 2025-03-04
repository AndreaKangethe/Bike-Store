from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def average_rating(reviews):
    avg = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg is None:
        return "No Ratings Yet"
    return round(avg, 1)  # Keep 1 decimal place
