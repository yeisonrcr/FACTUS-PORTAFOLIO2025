import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import json
import time

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("factus_client.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

class FactusClient:
    """Cliente mejorado para interactuar con la API de Factus usando autenticación OAuth2"""

    def __init__(self):
        """Inicializar el cliente de la API de Factus con configuración de autenticación"""
        self.base_url = "https://api-sandbox.factus.com.co"
        self.client_id = "9de7b800-6270-4567-81e1-2759d6fcb554"
        self.client_secret = "0qSxXYi87rDwck7Ybn8Taj2tGh1IoH8MHoupnR6O"
        self.username = "sandbox@factus.com.co"
        self.password = "sandbox2024%"
        self.access_token = None
        self.refresh_token = None

        # Configurar estrategia de reintento
        retry_strategy = Retry(
            total=3,  # Número máximo de reintentos
            backoff_factor=1,  # Tiempo entre reintentos
            status_forcelist=[500, 502, 503, 504],  # Códigos HTTP para reintento
        )

        # Crear una sesión HTTP con reintentos configurados
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get_headers(self):
        """Obtener encabezados para solicitudes a la API"""
        if not self.access_token:
            self.obtener_token()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        logger.debug(f"Encabezados generados: {json.dumps(headers, indent=2)}")
        return headers

    def obtener_token(self):
        """Solicitar un token de acceso a la API"""
        try:
            url = f"{self.base_url}/oauth/token"
            data = {
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
            }
            headers = {"Accept": "application/json"}

            logger.info("Solicitando token de acceso...")
            response = self.session.post(url, data=data, headers=headers)

            # Introducir un retardo
            time.sleep(2)

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                logger.info("Token de acceso obtenido exitosamente.")
                return token_data
            else:
                logger.error(f"Error obteniendo token. Status: {response.status_code}")
                logger.error(f"Respuesta: {response.text}")
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error en la solicitud del token: {str(e)}")
            raise

    def _handle_request(self, method, endpoint, **kwargs):
        """Manejar solicitudes HTTP con soporte para autenticación y reintentos"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers()
            kwargs["headers"] = headers

            logger.info(f"Realizando solicitud {method.__name__.upper()} a {url}")
            if "json" in kwargs:
                logger.debug(f"Payload: {json.dumps(kwargs['json'], indent=2)}")

            response = method(url, **kwargs)

            # Introducir un retardo entre solicitudes
            time.sleep(2)

            # Manejar token expirado (401)
            if response.status_code == 401:
                logger.info("Token expirado, renovando...")
                self.obtener_token()
                headers = self._get_headers()
                kwargs["headers"] = headers
                response = method(url, **kwargs)

            # Manejar errores HTTP
            if response.status_code >= 400:
                logger.error(f"Error en la solicitud. Status: {response.status_code}")
                logger.error(f"Respuesta: {response.text}")
                response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error en la solicitud a {endpoint}: {str(e)}")
            raise
