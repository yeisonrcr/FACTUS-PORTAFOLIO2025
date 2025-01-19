def prepare_factura_payload(factura, detalle):
    """
    Prepara el payload para la API de Factus según la documentación oficial
    """
    return {
        "document": "01",  # Factura electrónica de Venta
        "numbering_range_id": 4,  # Este valor debería ser configurable
        "reference_code": factura.numero_factura,  # Código de referencia de la factura
        "observation": "",  # Observación (vacío por defecto)
        "payment_form": "1",  # Pago de contado
        "payment_method_code": "10",  # Efectivo
        "customer": {
            "identification": factura.cliente.nit,  # NIT del cliente
            "dv": factura.cliente.dv if hasattr(factura.cliente, 'dv') else None,  # Dígito de verificación (opcional)
            "company": factura.cliente.razon_social,  # Razón social del cliente
            "trade_name": "",  # Nombre comercial (vacío por defecto)
            "names": "",  # Nombres (vacío por defecto)
            "address": factura.cliente.direccion,  # Dirección del cliente
            "email": factura.cliente.email,  # Email del cliente
            "phone": factura.cliente.telefono,  # Teléfono del cliente
            "legal_organization_id": "2",  # Este valor debería ser configurable
            "tribute_id": "21",  # Este valor debería ser configurable
            "identification_document_id": "3",  # Este valor debería ser configurable
            "municipality_id": "980"  # Este valor debería ser configurable
        },
        "items": [
            {
                "code_reference": detalle.codigo_referencia,  # Código de referencia del ítem
                "name": detalle.descripcion,  # Descripción del ítem
                "quantity": int(detalle.cantidad),  # Cantidad del ítem
                "discount_rate": 0,  # Tasa de descuento (0 por defecto)
                "price": float(detalle.valor_unitario),  # Precio unitario del ítem
                "tax_rate": "19.00",  # Este valor debería ser configurable
                "unit_measure_id": 70,  # Este valor debería ser configurable
                "standard_code_id": 1,  # Este valor debería ser configurable
                "is_excluded": 0,  # Indica si el ítem está excluido (0 por defecto)
                "tribute_id": 1,  # Este valor debería ser configurable
                "withholding_taxes": []  # Impuestos retenidos (vacío por defecto)
            }
        ]
    }
