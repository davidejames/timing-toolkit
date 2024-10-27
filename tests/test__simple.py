# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE

import pytest

from timing_toolkit.simple import (
    Defaults,
    timing,
)


def test__timing__bad_report_f():
    with pytest.raises(ValueError):
        timing(report_f = 2)


def test__timng__basic():

    calls = 0

    def _fake_timing():
        nonlocal calls
        calls += 1

    _saved_timing_func = Defaults.TIMING_FUNC
    Defaults.TIMING_FUNC = _fake_timing

    try:
        @timing()
        def foo():
            pass

        foo()
    finally:
        Defaults.TIMING_FUNC = _saved_timing_func

    assert calls == 2



def test__timing__report():

    calls = 0

    def _fake_timing():
        nonlocal calls
        calls += 1
        return calls

    _saved_timing_func = Defaults.TIMING_FUNC
    Defaults.TIMING_FUNC = _fake_timing

    reported_id = None
    reported_time = None

    def _report_f(id, elapsed):
        nonlocal reported_id
        nonlocal reported_time
        reported_id = id
        reported_time = elapsed

    try:
        @timing(report_f = _report_f)
        def foo():
            pass

        foo()
    finally:
        Defaults.TIMING_FUNC = _saved_timing_func

    assert calls         == 2
    assert reported_id   == 'foo'
    assert reported_time == 1


