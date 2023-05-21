import os
import logging
from unittest import mock

# Import your setup_logger function and CustomFormatter class
from src.log import setup_logger, CustomFormatter
from src import log

def test_setup_logger():
    # Test if logger is being setup correctly
    logger = log.setup_logger(__name__)

    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO

    handler_types = [type(handler) for handler in logger.handlers]

    assert logging.StreamHandler in handler_types
    assert all(isinstance(handler.formatter, CustomFormatter) for handler in logger.handlers)
    
    # Test if RotatingFileHandler is added when LOGGING is True
    with mock.patch.dict(os.environ, {"LOGGING": "True"}):
        logger = log.setup_logger(__name__)
        handler_types = [type(handler) for handler in logger.handlers]
        assert logging.handlers.RotatingFileHandler in handler_types # type: ignore

def test_logger_messages():
    # Test if logger is logging messages correctly
    logger = log.setup_logger(__name__)

    with mock.patch.object(logger, 'info') as mock_info:
        logger.info("Test info message")
        mock_info.assert_called_once_with("Test info message")

    with mock.patch.object(logger, 'warning') as mock_warning:
        logger.warning("Test warning message")
        mock_warning.assert_called_once_with("Test warning message")

    with mock.patch.object(logger, 'error') as mock_error:
        logger.error("Test error message")
        mock_error.assert_called_once_with("Test error message")

    with mock.patch.object(logger, 'critical') as mock_critical:
        logger.critical("Test critical message")
        mock_critical.assert_called_once_with("Test critical message")

def test_custom_formatter():
    formatter = CustomFormatter()
    record = logging.LogRecord(name='test', level=logging.INFO, pathname=None, lineno=None, msg=None, args=None, exc_info=None)
    formatted = formatter.format(record)

    assert '\x1b[34;1m' in formatted  # INFO level color code

    record.levelno = logging.WARNING
    formatted = formatter.format(record)

    assert '\x1b[33;1m' in formatted  # WARNING level color code
    

