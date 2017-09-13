Feature: add numbers
    In order to avoid silly mistakes
    As a math idiot
    I want to be told the sum of two numbers

    Scenario: Navigation to Home Page
        When I navigate to home page
        Then Home Page should be displayed

    Scenario: Add two numbers
        Given I navigate to home page
          And I have entered 50 as first number
          And I have entered 70 as second number
         When I press add
         Then 50 + 70 = 120 should be displayed        