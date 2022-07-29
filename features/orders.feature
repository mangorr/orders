Feature: The pet store service back-end
    As an E-Commerce Store Owner
    I need a RESTful orders service
    So that I can manage all customer orders

Background:
    Given the following orders
        | customer_id | tracking_id | created_time | status  | 
        | 4774        | 0798        | 2022-07-30   | SHIPPED |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order REST API Service" in the title
    And I should not see "404 Not Found"
