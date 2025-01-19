import logging
import uuid
from datetime import datetime
from factus_client import FactusClient

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('factus.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FactusTest:
    """Clase para realizar pruebas con la API de Factus."""
    
    def __init__(self):
        self.client = FactusClient()

    def create_test_invoice(self):
        """Crear una factura de prueba con datos específicos."""
        
        # Generar un código de referencia único para la factura
        reference_code = f"TEST-{uuid.uuid4().hex[:8]}"
        
        # Crear el payload con datos detallados
        invoice_payload = {
            "numbering_range_id": 4,
            "reference_code": reference_code,
            "observation": "Factura de prueba generada automáticamente",
            "payment_form": "1",  # Pago de contado
            "payment_due_date": "2024-12-30",  # Fecha límite de pago
            "payment_method_code": "10",  # Transferencia bancaria
            "billing_period": {
                "start_date": "2024-01-10",  # Fecha de inicio del periodo facturado
                "start_time": "00:00:00",  # Hora de inicio
                "end_date": "2024-02-09",  # Fecha de fin del periodo facturado
                "end_time": "23:59:59"  # Hora de fin
            },
            "customer": {
                "identification": "123456789",  # Número de identificación del cliente
                "dv": "3",  # Dígito de verificación (si aplica)
                "company": "",  # Nombre de la empresa (opcional)
                "trade_name": "",  # Nombre comercial (opcional)
                "names": "Alan Turing",  # Nombre del cliente
                "address": "calle 1 # 2-68",  # Dirección del cliente
                "email": "alanturing@enigmasas.com",  # Correo del cliente
                "phone": "1234567890",  # Teléfono del cliente
                "legal_organization_id": "2",  # Tipo de organización
                "tribute_id": "21",  # Código del régimen tributario
                "identification_document_id": "3",  # Tipo de documento
                "municipality_id": "980"  # ID del municipio
            },
            "items": [
                {
                    "code_reference": "12345",  # Código del producto
                    "name": "producto de prueba",  # Nombre del producto
                    "quantity": 1,  # Cantidad
                    "discount_rate": 20,  # Descuento (%)
                    "price": 50000,  # Precio unitario
                    "tax_rate": "19.00",  # Impuesto (%)
                    "unit_measure_id": 70,  # Unidad de medida
                    "standard_code_id": 1,  # Código estándar
                    "is_excluded": 0,  # Excluido de impuestos
                    "tribute_id": 1,  # ID del tributo
                    "withholding_taxes": [
                        {
                            "code": "06",  # Código de retención
                            "withholding_tax_rate": "7.00"  # Tasa de retención
                        },
                        {
                            "code": "05",
                            "withholding_tax_rate": "15.00"
                        }
                    ]
                },
                {
                    "code_reference": "54321",
                    "name": "producto de prueba 2",
                    "quantity": 1,
                    "discount_rate": 0,
                    "price": 50000,
                    "tax_rate": "5.00",
                    "unit_measure_id": 70,
                    "standard_code_id": 1,
                    "is_excluded": 0,
                    "tribute_id": 1,
                    "withholding_taxes": []
                }
            ]
        }

        try:
            logger.info("Obteniendo token de acceso...")
            token = self.client.obtener_token()
            if not token:
                raise RuntimeError("No se pudo obtener el token de acceso.")

            logger.info("Creando factura de prueba...")
            response = self.client.crear_factura(invoice_payload)
            logger.info(f"Factura creada exitosamente: {response}")

            return response

        except Exception as e:
            logger.error(f"Error en la creación de la factura: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    logger.info("=== Iniciando prueba de creación de factura en Factus ===")
    test = FactusTest()
    try:
        factura = test.create_test_invoice()
        logger.info(f"Resultado de la prueba: {factura}")
    except Exception as e:
        logger.error(f"Prueba fallida: {str(e)}")
