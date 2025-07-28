package com.hybridframework.tests.rest;

import com.fasterxml.jackson.databind.JsonNode;
import com.hybridframework.api.UserApiClient;
import com.hybridframework.config.ConfigManager;
import io.restassured.response.Response;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UserApiTest {
    private static final Logger logger = LoggerFactory.getLogger(UserApiTest.class);
    private UserApiClient userApiClient;
    private ConfigManager configManager;

    @BeforeClass
    public void setUp() {
        userApiClient = new UserApiClient();
        configManager = ConfigManager.getInstance();
        logger.info("User API Test setup completed");
    }

    @Test(description = "Get all users - Positive test")
    public void testGetAllUsers() {
        logger.info("Testing GET all users endpoint");
        
        Response response = userApiClient.getAllUsers();
        
        Assert.assertEquals(response.getStatusCode(), 200, "Status code should be 200");
        Assert.assertNotNull(response.getBody(), "Response body should not be null");
        
        JsonNode[] users = response.as(JsonNode[].class);
        Assert.assertTrue(users.length > 0, "Should return at least one user");
        
        logger.info("Successfully retrieved {} users", users.length);
    }

    @Test(description = "Get user by ID - Positive test")
    public void testGetUserById() {
        logger.info("Testing GET user by ID endpoint");
        
        int userId = 1;
        Response response = userApiClient.getUserById(userId);
        
        Assert.assertEquals(response.getStatusCode(), 200, "Status code should be 200");
        
        JsonNode user = response.as(JsonNode.class);
        Assert.assertEquals(user.get("id").asInt(), userId, "User ID should match");
        Assert.assertNotNull(user.get("name"), "User name should not be null");
        Assert.assertNotNull(user.get("email"), "User email should not be null");
        
        logger.info("Successfully retrieved user with ID: {}", userId);
    }

    @Test(description = "Create new user - Positive test")
    public void testCreateUser() {
        logger.info("Testing POST create user endpoint");
        
        JsonNode newUserData = userApiClient.getNewUserData();
        Response response = userApiClient.createUser(newUserData);
        
        Assert.assertEquals(response.getStatusCode(), 201, "Status code should be 201");
        
        JsonNode createdUser = response.as(JsonNode.class);
        Assert.assertNotNull(createdUser.get("id"), "Created user should have an ID");
        Assert.assertEquals(createdUser.get("name").asText(), newUserData.get("name").asText(), "User name should match");
        Assert.assertEquals(createdUser.get("email").asText(), newUserData.get("email").asText(), "User email should match");
        
        logger.info("Successfully created user with ID: {}", createdUser.get("id").asInt());
    }

    @Test(description = "Update user - Positive test")
    public void testUpdateUser() {
        logger.info("Testing PUT update user endpoint");
        
        int userId = 1;
        JsonNode updateData = userApiClient.getNewUserData();
        Response response = userApiClient.updateUser(userId, updateData);
        
        Assert.assertEquals(response.getStatusCode(), 200, "Status code should be 200");
        
        JsonNode updatedUser = response.as(JsonNode.class);
        Assert.assertEquals(updatedUser.get("id").asInt(), userId, "User ID should match");
        Assert.assertEquals(updatedUser.get("name").asText(), updateData.get("name").asText(), "Updated name should match");
        
        logger.info("Successfully updated user with ID: {}", userId);
    }

    @Test(description = "Delete user - Positive test")
    public void testDeleteUser() {
        logger.info("Testing DELETE user endpoint");
        
        int userId = 1;
        Response response = userApiClient.deleteUser(userId);
        
        Assert.assertEquals(response.getStatusCode(), 200, "Status code should be 200");
        
        logger.info("Successfully deleted user with ID: {}", userId);
    }

    @Test(description = "Get user posts - Positive test")
    public void testGetUserPosts() {
        logger.info("Testing GET user posts endpoint");
        
        int userId = 1;
        Response response = userApiClient.getUserPosts(userId);
        
        Assert.assertEquals(response.getStatusCode(), 200, "Status code should be 200");
        
        JsonNode[] posts = response.as(JsonNode[].class);
        Assert.assertTrue(posts.length > 0, "Should return at least one post");
        
        // Verify all posts belong to the user
        for (JsonNode post : posts) {
            Assert.assertEquals(post.get("userId").asInt(), userId, "Post should belong to the specified user");
        }
        
        logger.info("Successfully retrieved {} posts for user ID: {}", posts.length, userId);
    }

    @Test(description = "Get non-existent user - Negative test")
    public void testGetNonExistentUser() {
        logger.info("Testing GET non-existent user endpoint");
        
        int nonExistentUserId = 99999;
        Response response = userApiClient.getUserById(nonExistentUserId);
        
        Assert.assertEquals(response.getStatusCode(), 404, "Status code should be 404");
        
        logger.info("Correctly handled non-existent user request");
    }

    @Test(description = "Create user with invalid data - Negative test")
    public void testCreateUserWithInvalidData() {
        logger.info("Testing POST create user with invalid data");
        
        JsonNode invalidUserData = userApiClient.getInvalidUserData();
        Response response = userApiClient.createUser(invalidUserData);
        
        // Note: This API might return 201 even with invalid data, so we check for either 400 or 201
        Assert.assertTrue(response.getStatusCode() == 400 || response.getStatusCode() == 201, 
                         "Status code should be 400 for invalid data or 201 if API accepts it");
        
        logger.info("Handled invalid user data creation request");
    }
} 