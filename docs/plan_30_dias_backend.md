# Plan de 30 días — Backend Django para tienda online

## Objetivo del mes
Pasar de un backend funcional a uno profesional, automatizado y escalable, sin abrumarte.

## Semana 1 — Base sólida (orden + calidad)
- Definir estados claros del pedido (`carrito`, `pagado`, `enviado`, `entregado`, `cancelado`).
- Validaciones en backend (stock, cantidades, errores consistentes).
- Auditoría mínima (fechas, referencias de pago/envío, logs básicos).
- Tests iniciales de carrito, pedido y totales.

**Resultado:** backend estable y menos bugs.

## Semana 2 — Automatización sin IA (alto impacto)
- Limpieza de carritos abandonados y pedidos pendientes antiguos.
- Notificaciones automáticas de creación/cambio de estado de pedido.
- Reporte diario/semanal de ventas y productos top.
- Panel simple de “qué revisar hoy”.

**Resultado:** menos supervisión manual y mejor operación.

## Semana 3 — Integraciones API reales (nivel pro)
- API de pagos en sandbox y persistencia de estado.
- API de envíos (costo, guía y tracking).
- API de notificaciones (email, WhatsApp/SMS opcional).
- Reintentos automáticos y cola de errores.

**Resultado:** flujo completo de compra automatizado.

## Semana 4 — IA aplicada (práctica y útil)
- Clasificador de pedidos prioritarios/sospechosos.
- Asistente para preguntas frecuentes de clientes.
- Recomendaciones básicas de productos.
- Dashboard ejecutivo (conversión, ticket promedio, abandono).
- Cierre profesional (documentación y checklist de producción).

**Resultado:** operación semiautomática con IA y control humano en excepciones.

## Prioridades si tienes poco tiempo
1. Estados + validaciones + tests básicos.
2. Notificaciones automáticas + tareas programadas.
3. Integración de pagos/envíos en sandbox.
