import httpretty
import pytest


@pytest.fixture(name='httpretty')
def mockhttp():
    httpretty.enable()

    yield httpretty

    httpretty.disable()
    httpretty.reset()
