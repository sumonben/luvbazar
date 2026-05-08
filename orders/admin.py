from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem
from import_export.admin import ExportActionMixin,ImportExportMixin
from region.models import Division,District,Union,Upazilla


class DivisionFilter(admin.SimpleListFilter):
    title = 'Division'
    parameter_name = 'division'

    def lookups(self, request, model_admin):
        divisions = Division.objects.all().order_by('name')
        return [(d.id, d.name_en) for d in divisions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(division__id__exact=self.value())
        return queryset


class DistrictFilter(admin.SimpleListFilter):
    title = 'District'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = District.objects.all().order_by('name_en')
        return [(d.id, f"{d.name_en}") for d in districts]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(district__id__exact=self.value())
        return queryset


class UpazillaFilter(admin.SimpleListFilter):
    title = 'Upazilla'
    parameter_name = 'upazilla'

    def lookups(self, request, model_admin):
        upazillas = Upazilla.objects.all().order_by('name_en')
        return [(u.id, f"{u.name_en}") for u in upazillas]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(upazilla__id__exact=self.value())
        return queryset


class UnionFilter(admin.SimpleListFilter):
    title = 'Union'
    parameter_name = 'union'

    def lookups(self, request, model_admin):
        unions = Union.objects.all().order_by('name_en')
        return [(u.id, f"{u.name_en}") for u in unions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(union__id__exact=self.value())
        return queryset


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total']


@admin.register(Order)
class OrderAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', DivisionFilter, DistrictFilter, UpazillaFilter, UnionFilter]
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'subtotal', 'total']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'union', 'upazilla', 'district', 'division')
        }),
        ('Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
