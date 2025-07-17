import logging
import logging.config
import yaml
import os
import inspect

def setup_logging(default_filename='logging.yaml', default_level=logging.INFO):
    """Set up logging configuration from a YAML file located in the `etc` directory relative to the caller's script."""

    # Get the caller's script directory
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    caller_dir = os.path.dirname(os.path.abspath(caller_file))

    # Build the path to the logging configuration file
    config_path = os.path.join(caller_dir, '..', 'etc', default_filename)

    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.config.dictConfig(config)
    else:
        print(f"Logging configuration file not found at {config_path}. Using default level.")
        logging.basicConfig(level=default_level)
