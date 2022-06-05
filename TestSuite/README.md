This project has been made using Python3. The project consists of one file (testsuite.py) that includes all tests,
and another file (common_methods.py) with functions and variable needed by the tests.
use in the tests (common_methods.py):
   * testsuite.py - Test Suite for the features
   * common_methods.py - Methods used by the tests
   * venv virtual environment with nosetests installed

 Requirements:

nosetests>=1.3.7
requests>=2.21.0

In order to run the test cases in a console, follow the steps:

* API wallbox-challenge-2022 must be up and running in local.
More info in https://github.com/josecrespo32/wallbox-challenge-2022/blob/main/README.md

* Python3 must be installed and used for this project
* virtualenv must be installed in the machine:
    · pip3 install virtualenv
* Create a virtual environment in the project folder:
   · cd BookerTests
   · virtualenv venv --system-site-packages

* Activate virtual environment:
   · source venv/bin/activate

* In the virtual environment, install nosetest and selenium (no need if using venv previously created)
   · sudo easy_install nose

* To run all tests in the folder (all the tests in this project are in TestSuite):
   · cd TestSuite
   · nosetests -v

* To run one single test:
  · nosetests -v file_name.py:ClassName.method_name
  · nosetests -v testsuite.py:TestsCreateToken.test_01_correct_login

* Once finished, virtual environment can be deactivated:
  · deactivate


Tests can also be run in PyCharm or other IDE. In Run configuration, choose Nosetests, and choose to run a whole folder
a file or a method. In working directory, set TestSuite folder.