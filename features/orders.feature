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
       | 9898        | 3434        | 2022-08-01   | DELIVERED  |
       | 7479        | 0000        | 2022-08-02   | PLACED  |
    Given the following items
       | order_id_index    | product_id  | quantity     | price   |
       | 0           | 6447        | 6            | 32      |
       | 0           | 2343        | 1            | 16      |
       | 2           | 5354        | 5            | 21      |


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

Scenario: Read an Order
    When I visit the "Home Page"
    And I check the "Customer ID" in the "Query" Area
    And I set the "query" to "4666"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "0" in the "Tracking ID" field
    And I should see "PLACED" in the "Status" dropdown
    When I copy the "Order Id" field
    And I press the "Clear" button
    And I paste the "Order Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "0" in the "Tracking ID" field
    And I should see "PLACED" in the "Status" dropdown
    And I should see "4666" in the "Customer ID" field
    And I should not see "404 Not Found"

Scenario: Cancel an order
        When I visit the "Home Page"
        And I check the "Customer ID" in the "Query" Area
        And I set the "query" to "7479"
        And I press the "Search" button
        Then I should see the message "Success"
        And I should see "0" in the "Tracking ID" field
        And I should see "PLACED" in the "Status" dropdown
        When I press the "Cancel" button
        Then I should see the message "Order has been CANCELLED!"
        When I check the "Customer ID" in the "Query" Area
        And I set the "query" to "7479"
        And I press the "Search" button
        Then I should see the message "Success"
        And I should see "CANCELLED" in the "Status" dropdown

Scenario: List all orders
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "4774" in the results
    And I should see "4798" in the results
    And I should see "SHIPPED" in the results
    And I should see "2333" in the results
    And I should see "0" in the results
    And I should see "PLACED" in the results
    And I should see "9898" in the results
    And I should see "3434" in the results
    And I should see "DELIVERED" in the results
    And I should see "7479" in the results
    And I should see "0" in the results
    And I should see "PLACED" in the results
    And I should not see "989877" in the results
    And I should not see "343434" in the results
    And I should not see "CANCELLED" in the results

Scenario: Update a Order
    When I visit the "Home Page"
    And I check the "Customer ID" in the "Query" Area
    And I set the "query" to "2333"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "0" in the "Tracking ID" field
    And I should see "PLACED" in the "Status" dropdown
    When I change "Tracking ID" to "556612"
    And I select "SHIPPED" in the "Status" dropdown
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Order Id" field
    And I press the "Clear" button
    And I paste the "Order Id" field
    And I press the "Retrieve" button
    Then I should see "556612" in the "Tracking ID" field
    When I press the "Clear" button
    And I press the "List" button
    Then I should see "556612" in the results

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
