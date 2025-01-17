import requests

class FactusClient:
    def __init__(self, client_id, client_secret, base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.access_token = None

    def obtener_token(self):
        """Obtiene un token de acceso desde la API de Factus."""
        url = f"{self.base_url}/oauth/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            return token_data
        else:
            raise Exception(f"Error al obtener token: {response.status_code} - {response.text}")

    def validar_factura(self, payload):
        """Envía los datos de la factura a la API para su validación."""
        if not self.access_token:
            self.obtener_token()

        url = f"{self.base_url}/facturas/validar"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al validar factura: {response.status_code} - {response.text}")
