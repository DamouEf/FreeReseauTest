from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'zone', 'priority', 'created_by')
    list_filter = ('zone', 'priority', 'created_by')

admin.site.register(Ticket, TicketAdmin)
