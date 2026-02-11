from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "nombre", "precio", "cantidad")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "estado", "total", "nombre", "apellido", "buy_order")
    list_filter = ("estado", "created_at")
    search_fields = ("id", "nombre", "apellido", "email", "telefono", "buy_order", "tbk_token")
    readonly_fields = ("created_at", "buy_order", "tbk_token")
    inlines = [OrderItemInline]

    actions = ["marcar_en_preparacion", "marcar_en_despacho", "marcar_entregada", "marcar_cancelada"]

    @admin.action(description="Marcar como En preparación")
    def marcar_en_preparacion(self, request, queryset):
        queryset.update(estado="en_preparacion")

    @admin.action(description="Marcar como En despacho")
    def marcar_en_despacho(self, request, queryset):
        queryset.update(estado="en_despacho")

    @admin.action(description="Marcar como Entregada")
    def marcar_entregada(self, request, queryset):
        queryset.update(estado="entregada")

    @admin.action(description="Marcar como Cancelada")
    def marcar_cancelada(self, request, queryset):
        queryset.update(estado="cancelada")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "nombre", "cantidad", "precio", "product")
    search_fields = ("order__id", "nombre", "order__buy_order")
