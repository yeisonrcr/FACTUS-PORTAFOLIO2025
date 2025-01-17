import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)



class FactusClient:
    """Client for interacting with the Factus API using OAuth2 authentication"""
    
    def __init__(self):
        """Initialize the Factus API client with configuration from settings"""
        self.base_url = 'https://api-sandbox.factus.com.co'
        self.client_id = '9de7b800-6270-4567-81e1-2759d6fcb554'
        self.client_secret = '0qSxXYi87rDwck7Ybn8Taj2tGh1IoH8MHoupnR6O'
        self.username = 'sandbox@factus.com.co'   # username es el email
        self.password = 'sandbox2024%'
        self.access_token = None
        self.refresh_token = None

    def _get_headers(self):
        """Get headers for API requests"""
        if not self.access_token:
            self.obtener_token()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def obtener_token(self):
        """Obtain access token from Factus API using password grant type"""
        try:
            url = f"{self.base_url}/oauth/token"
            
            # Los datos deben enviarse como form-data, no como JSON
            data = {
                'grant_type': 'password',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.username,
                'password': self.password
            }
            
            headers = {
                'Accept': 'application/json'
            }
            
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            logger.info("Token de acceso obtenido exitosamente")
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo token: {str(e)}")
            if hasattr(e.response, 'json'):
                try:
                    error_detail = e.response.json()
                    logger.error(f"Detalle del error: {error_detail}")
                except ValueError:
                    logger.error(f"Respuesta raw del error: {e.response.text}")
            raise

    def refresh_access_token(self):
        """
        Si el token expira (después de 1 hora), obtenemos uno nuevo
        En este caso, simplemente obtenemos un nuevo token en lugar de usar refresh token
        """
        return self.obtener_token()

    def _handle_request(self, method, endpoint, **kwargs):
        """Helper method to handle requests with token refresh"""
        try:
            headers = self._get_headers()
            kwargs['headers'] = headers
            
            response = method(f"{self.base_url}{endpoint}", **kwargs)
            
            # Si el token expiró (401), intentamos renovarlo una vez
            if response.status_code == 401:
                self.refresh_access_token()
                headers = self._get_headers()
                kwargs['headers'] = headers
                response = method(f"{self.base_url}{endpoint}", **kwargs)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en request a {endpoint}: {str(e)}")
            if hasattr(e.response, 'json'):
                try:
                    error_detail = e.response.json()
                    logger.error(f"Detalle del error: {error_detail}")
                except ValueError:
                    logger.error(f"Respuesta raw del error: {e.response.text}")
            raise

    def crear_factura(self, payload):
        """Create a new invoice in Factus"""
        return self._handle_request(requests.post, '/v1/bills/validate', json=payload)

    def validar_factura(self, factura_id):
        """Validate an invoice with Factus and DIAN"""
        return self._handle_request(requests.post, f'/v1/bills/validate/{factura_id}')

    def consultar_factura(self, factura_id):
        """Query invoice details from Factus"""
        return self._handle_request(requests.get, f'/v1/bills/{factura_id}')
    



if __name__ == "__main__":
    client = FactusClient()
    token = client.obtener_token()
    print(token)  # Debería mostrar access_token y refresh_token