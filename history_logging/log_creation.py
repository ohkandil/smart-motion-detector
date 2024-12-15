import logging

def setup_logger(log_file):
    logger = logging.getLogger('motion_detector')
    logger.setLevel(logging.INFO)
    
    # Create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(handler)
    
    return logger

def log_motion_event(logger, event):
    logger.info(event)

if __name__ == "__main__":
    log_file = 'motion_events.log'
    logger = setup_logger(log_file)
    
    # Example usage
    log_motion_event(logger, "Motion detected.")
