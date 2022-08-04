import os
import random

import pytest
import logging
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    if os.environ.get('PYTEST_CURRENT_TEST') is not None:
        current_test = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[current_test] = result.outcome


def pytest_sessionfinish(session):
    build = random.randint(0, 10000)
    for test in session.results:
        logger.info("RRRRR" + str(test) + " --- " + str(session.results[test]))
        obj = {"build_no": build, "test_case": test, "status": str(session.results[test])}
        # fobj = {1}
        result = requests.post(
            url="https://search-my-result-2ss2q3kyyz3gswafk4u3oajjdy.us-east-2.es.amazonaws.com/test_executions_1/sample_tests",
            auth=HTTPBasicAuth('xxxx', 'xxxxx'),
            json=obj
        )
        logger.info(result.status_code)
        logger.info(result.json())
        logger.info(build)

    # myobj = {build: session.results}
    # result = requests.post(
    #     url="https://search-my-result-2ss2q3kyyz3gswafk4u3oajjdy.us-east-2.es.amazonaws.com/test_results_1/sample_tests",
    #     auth=HTTPBasicAuth('admin', 'Admin@123'),
    #     json=myobj
    # )
    # logger.info(result.status_code)
    # logger.info(result.json())

# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#
#     # set a report attribute for each phase of a call, which can
#     # be "setup", "call", "teardown"
#
#     setattr(item, "rep_" + rep.when, rep)
#
# @pytest.fixture(scope="function", autouse=True)
# def run_before_and_after_tests(request):
#     """Fixture to execute asserts before and after a test is run"""
#     # Setup: fill with any logic you want
#     logger.info("running: " + os.environ.get('PYTEST_CURRENT_TEST'))
#     logger.info(os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0])
#     current_test = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
#     status = "running"
#
#     yield # this is where the testing happens
#
#     if request.node.rep_setup.failed:
#         logger.info("setting up a test failed!", request.node.nodeid)
#     elif request.node.rep_setup.passed:
#         if request.node.rep_call.failed:
#             logger.info("executing test failed", request.node.nodeid)
#
#
#
#     # Teardown : fill with any logic you want
