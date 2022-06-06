This folder includes an postman collection with tests for API.

Test cases can be run by importing WallBox.postman_collection.0606.json in Postman, or using newman in Terminal.

In order to run the test cases in Terminal:

1. Install newman:


    npm install -g newman


2. Run the collection (indicating correct path if not located in same folder as collection file):

    newman run WallBox.postman_collection.json


Before running the collection, API wallbox-challenge-2022 must be up and running in local.
More info in https://github.com/josecrespo32/wallbox-challenge-2022/blob/main/README.md