"""
Ticket models for the helpdesk application.
"""
from django.db import models
from django.utils import timezone
from apps.users.models import User


class Ticket(models.Model):
    """
    Ticket model for support requests.
    """
    STATUS_CHOICES = [
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
        ('canceled', 'Cancelado'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    image = models.ImageField(
        upload_to='ticket_images/',
        null=True,
        blank=True,
        help_text='Imagen adjunta al ticket'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tickets'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.id} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Set resolved_at when status changes to resolved
        if self.pk:
            old_ticket = Ticket.objects.get(pk=self.pk)
            if (old_ticket.status != 'resolved' and 
                self.status == 'resolved' and 
                not self.resolved_at):
                self.resolved_at = timezone.now()
        elif self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def display_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    @property
    def display_priority(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority, self.priority)
