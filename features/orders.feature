Feature: The pet store service back-end
    As an E-Commerce Store Owner
    I need a RESTful orders service
    So that I can manage all customer orders

Background:
    Given the following orders
       | customer_id | tracking_id | created_time | status  |
       | 4774        | 4798        | 2022-07-30   | SHIPPED |
       | 2333        | 0000        | 2022-07-21   | PLACED  |
       | 4666        | 0000        | 2022-07-01   | PLACED  |
    # Given the following items
    #    | order_id    | product_id  | quantity     | price   |
    #    | 1000           | 6447        | 6            | 32      |
    #    | 1000           | 2343        | 1            | 16      |
    #    | 1020           | 5354        | 5            | 21      |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a new Order
    When I visit the "Home Page"
    And I check the "Customer ID" in the "Query" Area
    And I set the "query" to "1234"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "1234" in the results    
    When I press the "Clear" button
    And I set the "Customer ID" to "1234"
    And I set the "Tracking ID" to "0"
    And I select "PAID" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Order ID" field
    And I press the "Clear" button
    Then the "Order ID" field should be empty
    And the "Customer_ID" field should be empty
    And the "Tracking ID" field should be empty
    When I paste the "Order ID" field
    And I press the "Retrieve" button
    Then I should see "1234" in the "Customer_ID" field
    And I should see "0" in the "Tracking ID" field
    And I should see "PAID" in the "Status" dropdown

Scenario: Delete an Order
    When I visit the "Home Page"
    And I check the "Customer ID" in the "Query" Area
    And I set the "query" to "4666"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "0" in the "Tracking ID" field
    And I should see "PLACED" in the "Status" dropdown
    When I press the "Delete" button
    Then I should see the message "Order has been Deleted!"
    When I check the "Customer ID" in the "Query" Area
    And I set the "query" to "4666"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "4666" in the results

Scenario: Query orders by customer ID
    When I visit the "Home Page"
    And I check the "Customer ID" in the "Query" Area
    And I set the "query" to "4774"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "4774" in the results
    And I should see "4798" in the results
    And I should see "SHIPPED" in the results
    And I should see "SHIPPED" in the "Status" dropdown
    And I should not see "404 Not Found"
    And I should not see "4666" in the results    And I should not see "2333" in the results
    
Scenario: Query orders by Status
    When I visit the "Home Page"
    And I check the "Status" in the "Query" Area
    And I set the "query" to "PLACED"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "2333" in the results
    And I should see "4666" in the results
    And I should see "0" in the results
    And I should not see "404 Not Found"
