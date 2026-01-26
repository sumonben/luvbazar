from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'method', 'status', 'amount', 'transaction_id', 'created_at']
    list_filter = ['method', 'status', 'created_at']
    search_fields = ['order__order_number', 'transaction_id', 'sslc_val_id', 'sslc_tran_id']
    readonly_fields = ['created_at', 'updated_at', 'processed_at', 'transaction_id', 'sslc_val_id', 'sslc_tran_id']
    
    fieldsets = (
        ('Order & Amount', {
            'fields': ('order', 'amount')
        }),
        ('Payment Method', {
            'fields': ('method', 'status')
        }),
        ('Transaction Information', {
            'fields': ('transaction_id', 'sslc_val_id', 'sslc_tran_id', 'bank_tran_id')
        }),
        ('Card Details', {
            'fields': ('card_type', 'card_issuer', 'card_number'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual payment creation"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent payment deletion"""
        return False
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'method', 'status', 'amount')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'processed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
