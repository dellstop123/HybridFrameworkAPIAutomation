package com.hybridframework.config;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class ConfigManager {
    private static final Logger logger = LoggerFactory.getLogger(ConfigManager.class);
    private static ConfigManager instance;
    private JsonNode environmentConfig;
    private JsonNode testDataConfig;
    private String currentEnvironment;

    private ConfigManager() {
        loadConfigurations();
    }

    public static ConfigManager getInstance() {
        if (instance == null) {
            instance = new ConfigManager();
        }
        return instance;
    }

    private void loadConfigurations() {
        try {
            ObjectMapper mapper = new ObjectMapper();
            
            // Load environment configuration
            String envConfigPath = "src/main/resources/config/environment.json";
            environmentConfig = mapper.readTree(new File(envConfigPath));
            
            // Load test data configuration
            String testDataPath = "src/main/resources/config/testdata.json";
            testDataConfig = mapper.readTree(new File(testDataPath));
            
            // Set default environment
            currentEnvironment = System.getProperty("env", "dev");
            
            logger.info("Configuration loaded successfully for environment: {}", currentEnvironment);
        } catch (IOException e) {
            logger.error("Error loading configuration files", e);
            throw new RuntimeException("Failed to load configuration", e);
        }
    }

    public String getBaseUrl() {
        return environmentConfig.get(currentEnvironment).get("baseUrl").asText();
    }

    public int getTimeout() {
        return environmentConfig.get(currentEnvironment).get("timeout").asInt();
    }

    public int getRetryAttempts() {
        return environmentConfig.get(currentEnvironment).get("retryAttempts").asInt();
    }

    public JsonNode getHeaders() {
        return environmentConfig.get(currentEnvironment).get("headers");
    }

    public JsonNode getAuth() {
        return environmentConfig.get(currentEnvironment).get("auth");
    }

    public JsonNode getDatabase() {
        return environmentConfig.get(currentEnvironment).get("database");
    }

    public JsonNode getTestData(String key) {
        return testDataConfig.get(key);
    }

    public String getCurrentEnvironment() {
        return currentEnvironment;
    }

    public void setEnvironment(String environment) {
        if (environmentConfig.has(environment)) {
            this.currentEnvironment = environment;
            logger.info("Environment switched to: {}", environment);
        } else {
            logger.error("Environment '{}' not found in configuration", environment);
            throw new IllegalArgumentException("Invalid environment: " + environment);
        }
    }

    public String getApiEndpoint(String endpointKey) {
        return testDataConfig.get("api_endpoints").get(endpointKey).asText();
    }

    public JsonNode getTestScenario(String scenarioKey) {
        return testDataConfig.get("test_scenarios").get(scenarioKey);
    }
} 