from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import Ticket
from api.serializer import TicketSerializer

BASE_URL: str = "/api/v1/"

class TicketAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.ticket1 = Ticket.objects.create(
            priority=1, zone='A', created_by=self.user)
        self.ticket2 = Ticket.objects.create(
            priority=2, zone='B', created_by=User.objects.create_user(
                username='otheruser', password='otherpassword'))
        self.valid_payload = {
            'priority': 3,
            'zone': 'C'
        }
        self.invalid_payload = {
            'priority': 4
        }

    def test_get_own_tickets(self):
        response = self.client.get(reverse('tickets-list'))
        tickets = Ticket.objects.filter(created_by=self.user)
        serializer = TicketSerializer(tickets, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_get_other_tickets(self):
        self.client.force_authenticate(
            user=User.objects.create_user(
                username='someuser', password='somepassword'))
        response = self.client.get(reverse('tickets-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_ticket(self):
        response = self.client.post(
            reverse('tickets-list'),
            data=self.valid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_invalid_payload(self):
        response = self.client.post(
            reverse('tickets-list'),
            data=self.invalid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_own_ticket(self):
        response = self.client.put(
            reverse('tickets-detail', args=[self.ticket1.id]),
            data=self.valid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_other_ticket(self):
        response = self.client.put(
            reverse('tickets-detail', args=[self.ticket2.id]),
            data=self.valid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_ticket(self):
        response = self.client.delete(
            reverse('tickets-detail', args=[self.ticket1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_other_ticket(self):
        response = self.client.delete(
            reverse('tickets-detail', args=[self.ticket2.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TicketFilterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.tickets = [
            Ticket.objects.create(priority=1, zone='A', created_by=self.user),
            Ticket.objects.create(priority=2, zone='B', created_by=self.user),
            Ticket.objects.create(priority=3, zone='C', created_by=self.user),
            Ticket.objects.create(priority=4, zone='A', created_by=self.user),
            Ticket.objects.create(priority=5, zone='B', created_by=self.user),
            Ticket.objects.create(priority=6, zone='C', created_by=self.user),
            Ticket.objects.create(priority=7, zone='A', created_by=self.user),
            Ticket.objects.create(priority=8, zone='B', created_by=self.user),
            Ticket.objects.create(priority=9, zone='C', created_by=self.user),
            Ticket.objects.create(priority=10, zone='A', created_by=self.user),
        ]

    def test_filter_by_zone(self):
        url = reverse('tickets-list')
        response = self.client.get(url, {'zone': 'A'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        for ticket in response.data:
            self.assertEqual(ticket['zone'], 'A')