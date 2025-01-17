def prepare_factura_payload(factura, detalle):
    """
    Prepara el payload para la API de Factus según la documentación oficial
    """
    return {
        "document": "01",  # Factura electrónica de Venta
        "numbering_range_id": 4,  # Este valor debería ser configurable
        "reference_code": factura.numero_factura,
        "observation": "",
        "payment_form": "1",  # Pago de contado
        "payment_method_code": "10",  # Efectivo
        "customer": {
            "identification": factura.cliente.nit,
            "dv": factura.cliente.dv if hasattr(factura.cliente, 'dv') else None,
            "company": factura.cliente.razon_social,
            "trade_name": "",
            "names": "",
            "address": factura.cliente.direccion,
            "email": factura.cliente.email,
            "phone": factura.cliente.telefono,
            "legal_organization_id": "2",  # Este valor debería ser configurable
            "tribute_id": "21",  # Este valor debería ser configurable
            "identification_document_id": "3",  # Este valor debería ser configurable
            "municipality_id": "980"  # Este valor debería ser configurable
        },
        "items": [
            {
                "code_reference": detalle.codigo_referencia,
                "name": detalle.descripcion,
                "quantity": int(detalle.cantidad),
                "discount_rate": 0,
                "price": float(detalle.valor_unitario),
                "tax_rate": "19.00",  # Este valor debería ser configurable
                "unit_measure_id": 70,  # Este valor debería ser configurable
                "standard_code_id": 1,  # Este valor debería ser configurable
                "is_excluded": 0,
                "tribute_id": 1,  # Este valor debería ser configurable
                "withholding_taxes": []
            }
        ]
    }