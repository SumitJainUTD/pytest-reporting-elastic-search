import logging

logger = logging.getLogger(__name__)


class TestSample:

    def test_first(self):
        assert 4 == 4
        logger.info("this test is passed")

    def test_second(self):
        assert 4 == 4
        # logging.info("passed")

    def test_third(self):
        assert 4 == 3, "failed"

    def test_four(self):
        assert True
