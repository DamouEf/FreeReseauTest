
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .serializer import MyTokenObtainPairSerializer, TicketSerializer
from .models import Ticket
from .permissions import IsCreator
from api.base.filters import TicketFilter
from api.base.viewsets import BaseViewSet

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class TicketViewSet(BaseViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsCreator]
    filter_class = TicketFilter

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)