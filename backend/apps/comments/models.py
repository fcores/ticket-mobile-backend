"""
Comment models for the helpdesk application.
"""
from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.tickets.models import Ticket


class Comment(models.Model):
    """
    Comment model for ticket discussions.
    """
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.full_name} on #{self.ticket.id}"
