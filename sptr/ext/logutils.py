import logging

FMT_DEFAULT = logging.Formatter(
    fmt='%(asctime)s [%(name)s] %(levelname).4s %(message)s', datefmt='%H:%M:%S')


def setup_logging(debug=True, logfile=None):
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    formatter = FMT_DEFAULT

    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()

    root_logger = logging.getLogger()

    # Logger setup itself
    root_logger.setLevel(log_level)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    #logging.getLogger('googletrans').disabled = True
