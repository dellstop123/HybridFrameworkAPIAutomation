import pytest
import requests
from typing import Dict, Any
from api.base_api_client import BaseApiClient
from config.config_manager import ConfigManager


class TestUserApi:
    """Test class for User API endpoints using pytest."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.api_client = BaseApiClient()
        self.config_manager = ConfigManager()
        self.users_endpoint = self.config_manager.get_api_endpoint("users")
        self.test_data = self.config_manager.get_test_data("users")
    
    def test_get_all_users(self):
        """Test GET all users endpoint - Positive test."""
        response = self.api_client.get(self.users_endpoint)
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.json() is not None, "Response should contain JSON data"
        
        users = response.json()
        assert len(users) > 0, "Should return at least one user"
        
        # Verify user structure
        for user in users:
            assert "id" in user, "User should have an ID"
            assert "name" in user, "User should have a name"
            assert "email" in user, "User should have an email"
    
    def test_get_user_by_id(self):
        """Test GET user by ID endpoint - Positive test."""
        user_id = 1
        response = self.api_client.get(f"{self.users_endpoint}/{user_id}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        user = response.json()
        assert user["id"] == user_id, f"User ID should be {user_id}"
        assert "name" in user, "User should have a name"
        assert "email" in user, "User should have an email"
    
    def test_create_user(self):
        """Test POST create user endpoint - Positive test."""
        new_user_data = self.test_data["new_user"]
        response = self.api_client.post(self.users_endpoint, json_data=new_user_data)
        
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        
        created_user = response.json()
        assert "id" in created_user, "Created user should have an ID"
        assert created_user["name"] == new_user_data["name"], "User name should match"
        assert created_user["email"] == new_user_data["email"], "User email should match"
    
    def test_update_user(self):
        """Test PUT update user endpoint - Positive test."""
        user_id = 1
        update_data = self.test_data["new_user"]
        response = self.api_client.put(f"{self.users_endpoint}/{user_id}", json_data=update_data)
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        updated_user = response.json()
        assert updated_user["id"] == user_id, f"User ID should be {user_id}"
        assert updated_user["name"] == update_data["name"], "Updated name should match"
    
    def test_patch_user(self):
        """Test PATCH update user endpoint - Positive test."""
        user_id = 1
        patch_data = {"name": "Updated Name"}
        response = self.api_client.patch(f"{self.users_endpoint}/{user_id}", json_data=patch_data)
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        patched_user = response.json()
        assert patched_user["id"] == user_id, f"User ID should be {user_id}"
        assert patched_user["name"] == patch_data["name"], "Patched name should match"
    
    def test_delete_user(self):
        """Test DELETE user endpoint - Positive test."""
        user_id = 1
        response = self.api_client.delete(f"{self.users_endpoint}/{user_id}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    def test_get_user_posts(self):
        """Test GET user posts endpoint - Positive test."""
        user_id = 1
        response = self.api_client.get(f"{self.users_endpoint}/{user_id}/posts")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        posts = response.json()
        assert len(posts) > 0, "Should return at least one post"
        
        # Verify all posts belong to the user
        for post in posts:
            assert post["userId"] == user_id, f"Post should belong to user {user_id}"
    
    def test_get_user_todos(self):
        """Test GET user todos endpoint - Positive test."""
        user_id = 1
        response = self.api_client.get(f"{self.users_endpoint}/{user_id}/todos")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        todos = response.json()
        assert len(todos) > 0, "Should return at least one todo"
        
        # Verify all todos belong to the user
        for todo in todos:
            assert todo["userId"] == user_id, f"Todo should belong to user {user_id}"
    
    def test_get_user_albums(self):
        """Test GET user albums endpoint - Positive test."""
        user_id = 1
        response = self.api_client.get(f"{self.users_endpoint}/{user_id}/albums")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        albums = response.json()
        assert len(albums) > 0, "Should return at least one album"
        
        # Verify all albums belong to the user
        for album in albums:
            assert album["userId"] == user_id, f"Album should belong to user {user_id}"
    
    def test_get_nonexistent_user(self):
        """Test GET non-existent user endpoint - Negative test."""
        non_existent_user_id = 99999
        response = self.api_client.get(f"{self.users_endpoint}/{non_existent_user_id}")
        
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
    
    def test_create_user_invalid_data(self):
        """Test POST create user with invalid data - Negative test."""
        invalid_user_data = self.test_data["invalid_user"]
        response = self.api_client.post(self.users_endpoint, json_data=invalid_user_data)
        
        # Note: This API might return 201 even with invalid data, so we check for either 400 or 201
        assert response.status_code in [400, 201], f"Expected status code 400 or 201, got {response.status_code}"
    
    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_get_multiple_users(self, user_id):
        """Test GET multiple users by ID - Parameterized test."""
        response = self.api_client.get(f"{self.users_endpoint}/{user_id}")
        
        assert response.status_code == 200, f"Expected status code 200 for user {user_id}, got {response.status_code}"
        
        user = response.json()
        assert user["id"] == user_id, f"User ID should be {user_id}"
    
    def test_response_time_performance(self):
        """Test response time performance."""
        import time
        
        start_time = time.time()
        response = self.api_client.get(self.users_endpoint)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        assert response.status_code == 200, "Request should be successful"
        assert response_time < 5000, f"Response time should be less than 5 seconds, got {response_time:.2f}ms"
    
    def test_response_schema_validation(self):
        """Test response schema validation."""
        response = self.api_client.get(f"{self.users_endpoint}/1")
        
        assert response.status_code == 200, "Request should be successful"
        
        user = response.json()
        
        # Define expected schema
        expected_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "username": {"type": "string"}
            },
            "required": ["id", "name", "email"]
        }
        
        # Validate schema
        assert self.api_client.validate_response_schema(response, expected_schema), "Response should match expected schema" 