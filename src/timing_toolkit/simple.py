# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
'''A 'simple' timing module.

Easy way to add resilience and observability timing features to your
functions.
'''

from functools import wraps
import time


class Defaults:
    TIMING_FUNC = time.perf_counter



def timing(id=None, report_f=None, max=None):
    '''Decorator factory, enables timing features.

    - measures execution, reports to report_f
    - (soon) ability to limit max execution time

    '''
    if max is not None:
        raise NotImplementedError('timeout feature not yet implemented')

    if report_f is not None and not callable(report_f):
        raise ValueError(f'report_f must be None or callable')

    def _timing_decorator(func):

        _exec_id = id or func.__name__

        @wraps(func)
        def _timing_wrapper(*args, **kwargs):

            start = Defaults.TIMING_FUNC()

            return_val = func(*args, **kwargs)

            end = Defaults.TIMING_FUNC()

            if report_f is not None:
                try:
                    report_f(_exec_id, end-start)
                except Exception:
                    pass

            return return_val

        return _timing_wrapper
    return _timing_decorator


