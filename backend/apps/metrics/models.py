"""
Metrics models for the helpdesk application.
"""
from django.db import models
from django.utils import timezone


class SystemMetric(models.Model):
    """
    Model to store system metrics.
    """
    metric_name = models.CharField(max_length=100)
    metric_value = models.JSONField()
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'system_metrics'
        verbose_name = 'Métrica del Sistema'
        verbose_name_plural = 'Métricas del Sistema'
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.metric_name} - {self.recorded_at}"
