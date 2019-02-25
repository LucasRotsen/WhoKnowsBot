from datetime import datetime

from utils.file_utility import append


def log_error(error_message, method_name):
    date = str(datetime.now())
    message = "{datetime} - Error on '{method}': {error} \n".format(datetime=date, error=error_message,
                                                                    method=method_name)
    append('resources/errors_log.txt', message)


def log_retry(details):
    date = str(datetime.now())

    message = "{date} - Backing off {wait:0.1f} seconds afters {tries} tries calling function {target} \n" \
        .format(date=date, **details)

    append('resources/retries_log.txt', message)
