# Module:   test_timers
# Date:     10th February 2010
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""Timers Tests"""

import pytest

from datetime import datetime, timedelta

from circuits import Event, Component, Timer


def pytest_funcarg__app(request):
    return request.cached_setup(
        setup=lambda: setupapp(request),
        teardown=lambda app: teardownapp(app),
        scope="module"
    )


def setupapp(request):
    app = App()
    app.start()
    return app


def teardownapp(app):
    app.stop()


class Test(Event):
    """Test Event"""


class App(Component):

    flag = False

    def reset(self):
        self.flag = False

    def test(self):
        self.flag = True


def test_timer(app):
    timer = Timer(0.1, Test(), "timer")
    timer.register(app)
    assert pytest.wait_for(app, "flag")
    app.reset()


def test_persistentTimer(app):
    timer = Timer(0.2, Test(), "timer", persist=True)
    timer.register(app)

    for i in range(2):
        assert pytest.wait_for(app, "flag")
        app.reset()

    timer.unregister()


def test_datetime(app):
    now = datetime.now()
    d = now + timedelta(seconds=0.1)
    timer = Timer(d, Test(), "timer")
    timer.register(app)
    assert pytest.wait_for(app, "flag")
    app.reset()
