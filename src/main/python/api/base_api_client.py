import requests
import json
from typing import Dict, Any, Optional, Union
from loguru import logger
from config.config_manager import ConfigManager


class BaseApiClient:
    """Base API client providing common functionality for all API requests."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup the requests session with default configuration."""
        # Set base URL
        self.session.base_url = self.config_manager.get_base_url()
        
        # Set default headers
        headers = self.config_manager.get_headers()
        self.session.headers.update(headers)
        
        # Set authentication
        auth_token = self.config_manager.get_auth_token()
        if auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
        
        # Set timeout
        self.timeout = self.config_manager.get_timeout()
        
        logger.info(f"API client initialized for environment: {self.config_manager.get_current_environment()}")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a GET request."""
        url = f"{self.session.base_url}{endpoint}"
        logger.info(f"Making GET request to: {url}")
        if params:
            logger.info(f"Query parameters: {params}")
        
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
             json_data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a POST request."""
        url = f"{self.session.base_url}{endpoint}"
        logger.info(f"Making POST request to: {url}")
        
        response = self.session.post(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
            json_data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a PUT request."""
        url = f"{self.session.base_url}{endpoint}"
        logger.info(f"Making PUT request to: {url}")
        
        response = self.session.put(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def patch(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
              json_data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a PATCH request."""
        url = f"{self.session.base_url}{endpoint}"
        logger.info(f"Making PATCH request to: {url}")
        
        response = self.session.patch(url, data=data, json=json_data, headers=headers, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Make a DELETE request."""
        url = f"{self.session.base_url}{endpoint}"
        logger.info(f"Making DELETE request to: {url}")
        
        response = self.session.delete(url, headers=headers, timeout=self.timeout)
        self._log_response(response)
        return response
    
    def _log_response(self, response: requests.Response):
        """Log response details."""
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Time: {response.elapsed.total_seconds() * 1000:.2f} ms")
        
        if response.status_code >= 400:
            logger.error(f"Response Body: {response.text}")
        else:
            logger.debug(f"Response Body: {response.text}")
    
    def add_header(self, key: str, value: str):
        """Add a header to the session."""
        self.session.headers.update({key: value})
    
    def add_headers(self, headers: Dict[str, str]):
        """Add multiple headers to the session."""
        self.session.headers.update(headers)
    
    def set_auth_token(self, token: str):
        """Set authentication token."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def clear_auth_token(self):
        """Clear authentication token."""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def get_session_headers(self) -> Dict[str, str]:
        """Get current session headers."""
        return dict(self.session.headers)
    
    def set_timeout(self, timeout: int):
        """Set custom timeout for requests."""
        self.timeout = timeout
    
    def reset_session(self):
        """Reset the session to default configuration."""
        self.session = requests.Session()
        self._setup_session()
    
    def validate_response_status(self, response: requests.Response, expected_status: int) -> bool:
        """Validate if response status matches expected status."""
        return response.status_code == expected_status
    
    def validate_response_schema(self, response: requests.Response, schema: Dict) -> bool:
        """Validate response against JSON schema."""
        try:
            from jsonschema import validate
            response_json = response.json()
            validate(instance=response_json, schema=schema)
            return True
        except Exception as e:
            logger.error(f"Schema validation failed: {e}")
            return False
    
    def get_response_json(self, response: requests.Response) -> Optional[Dict]:
        """Safely get JSON response."""
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None 