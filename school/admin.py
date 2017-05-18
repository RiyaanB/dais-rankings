from django.contrib import admin
from school.models import Event
admin.site.site_header = "Dais Event Administration"
admin.site.site_title = "Dais Event Admin"
admin.site.register(Event)
#admin.site.register()