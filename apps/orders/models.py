from django.db import models
from apps.accounts.models import User


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    )

    SERVICE_CHOICES = (
        ('mariage', 'Mariage'),
        ('portrait', 'Portrait'),
        ('evenement', 'Événement'),
        ('autre', 'Autre'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_orders')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.client.username} → {self.photographer.username}"

    class Meta:
        ordering = ['-created_at']