"""
Attachment models for the helpdesk application.
"""
import os
from django.db import models
from django.utils import timezone
from django.utils.text import get_valid_filename
from apps.users.models import User
from apps.tickets.models import Ticket


def upload_attachment_to(instance, filename):
    """
    Generate upload path for attachments.
    """
    filename = get_valid_filename(filename)
    return os.path.join('uploads', 'attachments', f"{instance.ticket.id}", filename)


class Attachment(models.Model):
    """
    Attachment model for ticket files.
    """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_attachments'
    )
    file = models.FileField(upload_to=upload_attachment_to)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'attachments'
        verbose_name = 'Archivo Adjunto'
        verbose_name_plural = 'Archivos Adjuntos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_filename} (Ticket #{self.ticket.id})"
    
    @property
    def filename(self):
        return os.path.basename(self.file.name)
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.original_filename = self.file.name
            # Try to determine MIME type from file extension
            import mimetypes
            mime_type, _ = mimetypes.guess_type(self.file.name)
            self.mime_type = mime_type or 'application/octet-stream'
        super().save(*args, **kwargs)
