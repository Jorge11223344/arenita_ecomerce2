# payments/views.py
import os
import time
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from orders.models import Order

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys


logger = logging.getLogger(__name__)


def _tbk_tx() -> Transaction:
    env = (os.getenv("TBK_ENV") or "integration").strip().lower()
    commerce_code = (os.getenv("TBK_COMMERCE_CODE") or "").strip()
    api_key = (os.getenv("TBK_API_KEY") or "").strip()

    integration_type = (
        IntegrationType.LIVE
        if env in ("production", "live")
        else IntegrationType.TEST
    )

    # Credenciales propias (si están configuradas)
    if commerce_code and api_key:
        opts = WebpayOptions(commerce_code, api_key, integration_type)
        return Transaction(opts)

    # Integración / Sandbox
    opts = WebpayOptions(
        IntegrationCommerceCodes.WEBPAY_PLUS,
        IntegrationApiKeys.WEBPAY,
        IntegrationType.TEST,
    )
    return Transaction(opts)


# 🔁 INICIO DE PAGO (Order → Webpay)
def webpay_init(request, order_id):
    if request.method != "POST":
        return redirect("store")  # ajusta si tu url de tienda se llama distinto

    order = get_object_or_404(Order, id=order_id)

    # buy_order único y persistente
    buy_order = f"ORD-{order.id}-{int(time.time())}"
    amount = int(order.total)
    session_id = str(order.id)

    order.buy_order = buy_order
    order.save(update_fields=["buy_order"])

    public_base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    return_url = f"{public_base}{reverse('webpay_return')}"

    tx = _tbk_tx()
    resp = tx.create(buy_order, session_id, amount, return_url)

    # Guardar token Webpay
    if hasattr(order, "tbk_token"):
        order.tbk_token = resp["token"]
        order.save(update_fields=["tbk_token"])

    return render(request, "payments/redirect.html", {
        "action": resp["url"],
        "token": resp["token"],
    })


# 🔁 RETORNO DESDE WEBPAY
@csrf_exempt
def webpay_return(request):
    token = request.POST.get("token_ws") or request.GET.get("token_ws")

    # Cancelación o retorno inválido
    if not token:
        messages.error(request, "Pago cancelado o token inválido.")
        return render(request, "payments/resultado.html", {
            "ok": False,
            "order": None,
            "resp": {"status": "CANCELED"},
        })

    # Commit protegido
    try:
        tx = _tbk_tx()
        resp = tx.commit(token)
    except Exception as e:
        logger.exception("Error commit Webpay: %s", e)
        messages.error(request, "Error confirmando el pago con Transbank.")
        return render(request, "payments/resultado.html", {
            "ok": False,
            "order": None,
            "resp": {"status": "ERROR_COMMIT", "error": str(e)},
        })

    buy_order = resp.get("buy_order")
    status = resp.get("status")
    response_code = resp.get("response_code")

    ok = (status == "AUTHORIZED" and response_code == 0)

    # Si no viene buy_order, igual mostramos algo
    if not buy_order:
        if ok:
            messages.success(request, "¡Pago aprobado! Gracias por tu compra.")
        else:
            messages.error(request, f"Pago rechazado o anulado. Estado: {status}")
        return render(request, "payments/resultado.html", {
            "ok": ok,
            "order": None,
            "resp": resp,
        })

    order = get_object_or_404(Order, buy_order=buy_order)

    # Guardar token siempre (si existe el campo)
    if hasattr(order, "tbk_token"):
        order.tbk_token = token

    if ok:
        order.estado = "pagada"
        order.save(update_fields=["estado", "tbk_token"] if hasattr(order, "tbk_token") else ["estado"])
        Cart(request).clear()
        messages.success(request, "¡Pago aprobado! Gracias por tu compra.")
    else:
        order.estado = "fallida"
        order.save(update_fields=["estado", "tbk_token"] if hasattr(order, "tbk_token") else ["estado"])
        messages.error(request, f"Pago rechazado o anulado. Estado: {status}")

    return render(request, "payments/resultado.html", {
        "ok": ok,
        "order": order,
        "resp": resp,
    })
