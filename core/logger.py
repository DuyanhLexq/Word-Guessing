import logging

def log(log_name: str, level=logging.DEBUG, log_to_file=False, file_name="app.log") -> logging.Logger:
    """
    Create or get a logger by name.
    
    Args:
        log_name (str): The name of the logger.
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR).
        log_to_file (bool): If True, also log to a file.
        file_name (str): The log file name (used if log_to_file=True).
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Optional file handler
        if log_to_file:
            file_handler = logging.FileHandler(file_name)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
