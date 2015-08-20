
Introduction 
------------

This folder stores all unit tests for this Flask application.

<pre>
| File                      | Description                                          |
| ------------------------- | ----------------------------------------------------:|
| base_test.py              | Base class for unit tests                            |
| base_test_with_data.py    | Base class for unit tests with minimum database rows |
| test_*.py                 | Unit test files (must use the "test_" prefix)        |
</pre>


Setup
-------

To run tests easier we use the fabric tool:

<pre>
pip install fabric
cd app
fab prep_develop
</pre>


Usage
-----

Once you have installed the dependencies you can run the tests by executing:

<pre>
cd app
fab test
</pre>
