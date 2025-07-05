from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import Company, User


class DashboardWidget(models.Model):
    WIDGET_TYPES = (
        ('inventory_summary', _('Inventory Summary')),
        ('sales_summary', _('Sales Summary')),
        ('purchase_summary', _('Purchase Summary')),
        ('stock_alerts', _('Stock Alerts')),
        ('recent_movements', _('Recent Movements')),
        ('custom', _('Custom')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='dashboard_widgets',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=100)
    widget_type = models.CharField(
        _('Widget Type'),
        max_length=20,
        choices=WIDGET_TYPES
    )
    settings = models.JSONField(_('Settings'), default=dict)
    position = models.PositiveSmallIntegerField(_('Position'))
    is_visible = models.BooleanField(_('Visible'), default=True)

    class Meta:
        verbose_name = _('Dashboard Widget')
        verbose_name_plural = _('Dashboard Widgets')
        ordering = ['position']
        unique_together = ('company', 'position')

    def __str__(self):
        return self.name


class UserDashboard(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard',
        verbose_name=_('User')
    )
    layout = models.JSONField(_('Layout'), default=dict)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Dashboard')
        verbose_name_plural = _('User Dashboards')

    def __str__(self):
        return f"{self.user}'s Dashboard"