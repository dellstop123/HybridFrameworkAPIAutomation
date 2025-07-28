Feature: User Management API
  As a system administrator
  I want to manage users through the API
  So that I can perform CRUD operations on user data

  Background:
    Given the API base URL is configured
    And the API is accessible

  @positive @smoke
  Scenario: Get all users successfully
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should contain a list of users
    And each user should have required fields: id, name, email

  @positive @smoke
  Scenario: Get user by ID successfully
    Given a user with ID "1" exists
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response should contain user details
    And the user ID should be "1"
    And the user should have a name and email

  @positive
  Scenario: Create a new user successfully
    Given I have valid user data
    When I send a POST request to "/users" with the user data
    Then the response status code should be 201
    And the response should contain the created user details
    And the created user should have an ID
    And the user name and email should match the input data

  @negative
  Scenario: Get non-existent user
    Given a user with ID "99999" does not exist
    When I send a GET request to "/users/99999"
    Then the response status code should be 404

  @performance
  Scenario: API response time is acceptable
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response time should be less than 5 seconds 