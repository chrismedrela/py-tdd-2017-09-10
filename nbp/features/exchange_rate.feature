Feature: Exchange rate form
    In order to become rich
    As a future currency speculator
    I'd like to know currency exchange rates

    Scenario: Navigation to Home Page
        When I navigate to Home Page
        Then Home Page should be displayed

    Scenario Outline: Exchange rate form works
        Given I navigate to Home Page
          And I enter <date> as date
          And I enter <currency> as currency
         When I sent the form
         Then <expected output> should be displayed

    Examples:
      | date       | currency | expected output      |
      | 2017/02/03 | USD      | 1 USD = 4.0014 PLN   |
      | 2017/02/03 | ISK      | 100 ISK = 3.5263 PLN |
      | 2017/02/05 | USD      | No data for this day |
