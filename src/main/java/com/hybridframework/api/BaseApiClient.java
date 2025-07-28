package com.hybridframework.api;

import com.fasterxml.jackson.databind.JsonNode;
import com.hybridframework.config.ConfigManager;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

public class BaseApiClient {
    private static final Logger logger = LoggerFactory.getLogger(BaseApiClient.class);
    protected ConfigManager configManager;
    protected RequestSpecification requestSpec;

    public BaseApiClient() {
        this.configManager = ConfigManager.getInstance();
        setupBaseRequestSpec();
    }

    private void setupBaseRequestSpec() {
        requestSpec = RestAssured.given()
                .baseUri(configManager.getBaseUrl())
                .timeout(configManager.getTimeout())
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON);

        // Add default headers
        JsonNode headers = configManager.getHeaders();
        if (headers != null) {
            headers.fieldNames().forEachRemaining(key -> 
                requestSpec.header(key, headers.get(key).asText())
            );
        }

        // Add authentication if configured
        JsonNode auth = configManager.getAuth();
        if (auth != null && "bearer".equals(auth.get("type").asText())) {
            String token = auth.get("token").asText();
            if (token.startsWith("${") && token.endsWith("}")) {
                // Handle environment variable substitution
                String envVar = token.substring(2, token.length() - 1);
                token = System.getenv(envVar);
            }
            if (token != null && !token.isEmpty()) {
                requestSpec.header("Authorization", "Bearer " + token);
            }
        }
    }

    public Response get(String endpoint) {
        logger.info("Making GET request to: {}", endpoint);
        Response response = requestSpec.get(endpoint);
        logResponse(response);
        return response;
    }

    public Response get(String endpoint, Map<String, Object> queryParams) {
        logger.info("Making GET request to: {} with params: {}", endpoint, queryParams);
        RequestSpecification spec = requestSpec;
        queryParams.forEach(spec::queryParam);
        Response response = spec.get(endpoint);
        logResponse(response);
        return response;
    }

    public Response post(String endpoint, Object body) {
        logger.info("Making POST request to: {}", endpoint);
        Response response = requestSpec.body(body).post(endpoint);
        logResponse(response);
        return response;
    }

    public Response put(String endpoint, Object body) {
        logger.info("Making PUT request to: {}", endpoint);
        Response response = requestSpec.body(body).put(endpoint);
        logResponse(response);
        return response;
    }

    public Response patch(String endpoint, Object body) {
        logger.info("Making PATCH request to: {}", endpoint);
        Response response = requestSpec.body(body).patch(endpoint);
        logResponse(response);
        return response;
    }

    public Response delete(String endpoint) {
        logger.info("Making DELETE request to: {}", endpoint);
        Response response = requestSpec.delete(endpoint);
        logResponse(response);
        return response;
    }

    public Response delete(String endpoint, Object body) {
        logger.info("Making DELETE request to: {} with body", endpoint);
        Response response = requestSpec.body(body).delete(endpoint);
        logResponse(response);
        return response;
    }

    private void logResponse(Response response) {
        logger.info("Response Status: {}", response.getStatusCode());
        logger.info("Response Time: {} ms", response.getTime());
        if (response.getStatusCode() >= 400) {
            logger.error("Response Body: {}", response.getBody().asString());
        } else {
            logger.debug("Response Body: {}", response.getBody().asString());
        }
    }

    public RequestSpecification getRequestSpec() {
        return requestSpec;
    }

    public void addHeader(String key, String value) {
        requestSpec.header(key, value);
    }

    public void addHeaders(Map<String, String> headers) {
        headers.forEach(requestSpec::header);
    }

    public void setAuthToken(String token) {
        requestSpec.header("Authorization", "Bearer " + token);
    }

    public void setContentType(ContentType contentType) {
        requestSpec.contentType(contentType);
    }

    public void setAccept(ContentType contentType) {
        requestSpec.accept(contentType);
    }
} 