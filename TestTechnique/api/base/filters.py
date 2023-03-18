from api.models import Ticket
from django_filters import rest_framework as filters

class TicketFilter(filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {}
        for field in model._meta.fields:
            fields[field.name] = ['exact', 'lt', 'gt', 'in', 'isnull'] 