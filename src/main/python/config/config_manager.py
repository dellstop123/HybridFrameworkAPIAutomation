import json
import os
from typing import Dict, Any, Optional
from loguru import logger


class ConfigManager:
    """Configuration manager for handling environment and test data configuration."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.environment_config = {}
            self.test_data_config = {}
            self.current_environment = os.getenv('ENV', 'dev')
            self._load_configurations()
            self.initialized = True
    
    def _load_configurations(self):
        """Load environment and test data configurations from JSON files."""
        try:
            # Load environment configuration
            env_config_path = "src/main/resources/config/environment.json"
            with open(env_config_path, 'r') as f:
                self.environment_config = json.load(f)
            
            # Load test data configuration
            test_data_path = "src/main/resources/config/testdata.json"
            with open(test_data_path, 'r') as f:
                self.test_data_config = json.load(f)
            
            logger.info(f"Configuration loaded successfully for environment: {self.current_environment}")
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def get_base_url(self) -> str:
        """Get the base URL for the current environment."""
        return self.environment_config[self.current_environment]["baseUrl"]
    
    def get_timeout(self) -> int:
        """Get the timeout value for the current environment."""
        return self.environment_config[self.current_environment]["timeout"]
    
    def get_retry_attempts(self) -> int:
        """Get the retry attempts for the current environment."""
        return self.environment_config[self.current_environment]["retryAttempts"]
    
    def get_headers(self) -> Dict[str, str]:
        """Get the default headers for the current environment."""
        return self.environment_config[self.current_environment]["headers"]
    
    def get_auth(self) -> Dict[str, Any]:
        """Get the authentication configuration for the current environment."""
        return self.environment_config[self.current_environment]["auth"]
    
    def get_database(self) -> Dict[str, Any]:
        """Get the database configuration for the current environment."""
        return self.environment_config[self.current_environment]["database"]
    
    def get_test_data(self, key: str) -> Dict[str, Any]:
        """Get test data by key."""
        return self.test_data_config.get(key, {})
    
    def get_current_environment(self) -> str:
        """Get the current environment name."""
        return self.current_environment
    
    def set_environment(self, environment: str):
        """Set the current environment."""
        if environment in self.environment_config:
            self.current_environment = environment
            logger.info(f"Environment switched to: {environment}")
        else:
            logger.error(f"Environment '{environment}' not found in configuration")
            raise ValueError(f"Invalid environment: {environment}")
    
    def get_api_endpoint(self, endpoint_key: str) -> str:
        """Get API endpoint by key."""
        return self.test_data_config["api_endpoints"][endpoint_key]
    
    def get_test_scenario(self, scenario_key: str) -> Dict[str, Any]:
        """Get test scenario configuration by key."""
        return self.test_data_config["test_scenarios"][scenario_key]
    
    def get_auth_token(self) -> Optional[str]:
        """Get the authentication token for the current environment."""
        auth_config = self.get_auth()
        if auth_config.get("type") == "bearer":
            token = auth_config.get("token", "")
            if token.startswith("${") and token.endswith("}"):
                # Handle environment variable substitution
                env_var = token[2:-1]
                token = os.getenv(env_var)
            return token
        return None
    
    def get_all_environments(self) -> list:
        """Get list of all available environments."""
        return list(self.environment_config.keys())
    
    def get_environment_config(self, environment: str = None) -> Dict[str, Any]:
        """Get complete configuration for a specific environment."""
        env = environment or self.current_environment
        return self.environment_config.get(env, {}) 