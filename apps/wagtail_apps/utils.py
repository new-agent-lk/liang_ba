import datetime
import logging
import signal
import time
from functools import partial, wraps


def get_time_str(_time):
    time_str = ""
    if isinstance(_time, datetime.datetime) or isinstance(_time, datetime.date):
        time_str = _time.strftime("%Y%m%d")
    elif isinstance(_time, str):
        time_str = _time.replace("-", "")
    return time_str


def retry(times=-1, delay=0, timeout=10, exceptions=Exception, logger=logging.getLogger("scripts")):
    """
    :param times: 重试次数
    :param delay: 重试间隔时间
    :param exceptions: 想要捕获的错误类型
    :param logger: 指定日志对象输出
    :param timeout: 超时时间
    :return: func result or None
    """

    def _inter_retry(caller, retry_time, retry_delay, _time_out, es):
        while retry_time:

            def _handle_timeout(signum, frame):

                err_msg = f"Function {caller.func.__name__} timed out after {_time_out} seconds"
                raise TimeoutError(err_msg)

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(_time_out)
            try:
                return caller()
            except es as e:
                retry_time -= 1
                if not retry_time:
                    logger.error(
                        "max tries for {} times, {} is raised, details: func name is {}, func args are {}".format(
                            times, e, caller.func.__name__, (caller.args, caller.keywords)
                        )
                    )
                    raise
                time.sleep(retry_delay)
            finally:
                signal.alarm(0)

    def retry_decorator(func):
        @wraps(func)
        def _wraps(*args, **kwargs):
            return _inter_retry(partial(func, *args, **kwargs), times, delay, timeout, exceptions)

        return _wraps

    return retry_decorator
