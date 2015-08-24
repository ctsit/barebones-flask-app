Feature: testing the index page

Scenario: visit index and check the page title
When we visit index
Then it should have a title "Barebones Web Application"
