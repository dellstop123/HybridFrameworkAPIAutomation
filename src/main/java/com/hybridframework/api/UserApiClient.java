package com.hybridframework.api;

import com.fasterxml.jackson.databind.JsonNode;
import io.restassured.response.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

public class UserApiClient extends BaseApiClient {
    private static final Logger logger = LoggerFactory.getLogger(UserApiClient.class);
    private final String usersEndpoint;

    public UserApiClient() {
        super();
        this.usersEndpoint = configManager.getApiEndpoint("users");
    }

    public Response getAllUsers() {
        logger.info("Getting all users");
        return get(usersEndpoint);
    }

    public Response getUserById(int userId) {
        logger.info("Getting user with ID: {}", userId);
        return get(usersEndpoint + "/" + userId);
    }

    public Response getUserByEmail(String email) {
        logger.info("Getting user by email: {}", email);
        Map<String, Object> queryParams = new HashMap<>();
        queryParams.put("email", email);
        return get(usersEndpoint, queryParams);
    }

    public Response createUser(Object userData) {
        logger.info("Creating new user");
        return post(usersEndpoint, userData);
    }

    public Response updateUser(int userId, Object userData) {
        logger.info("Updating user with ID: {}", userId);
        return put(usersEndpoint + "/" + userId, userData);
    }

    public Response patchUser(int userId, Object userData) {
        logger.info("Patching user with ID: {}", userId);
        return patch(usersEndpoint + "/" + userId, userData);
    }

    public Response deleteUser(int userId) {
        logger.info("Deleting user with ID: {}", userId);
        return delete(usersEndpoint + "/" + userId);
    }

    public Response getUserPosts(int userId) {
        logger.info("Getting posts for user ID: {}", userId);
        return get(usersEndpoint + "/" + userId + "/posts");
    }

    public Response getUserTodos(int userId) {
        logger.info("Getting todos for user ID: {}", userId);
        return get(usersEndpoint + "/" + userId + "/todos");
    }

    public Response getUserAlbums(int userId) {
        logger.info("Getting albums for user ID: {}", userId);
        return get(usersEndpoint + "/" + userId + "/albums");
    }

    public JsonNode getValidUserData() {
        return configManager.getTestData("users").get("valid_user");
    }

    public JsonNode getNewUserData() {
        return configManager.getTestData("users").get("new_user");
    }

    public JsonNode getInvalidUserData() {
        return configManager.getTestData("users").get("invalid_user");
    }
} 