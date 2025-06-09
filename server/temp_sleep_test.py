import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting sleep test script...")
try:
    for i in range(60): # Sleep for 60 seconds, printing every second
        logger.info(f"Sleeping... {i+1}/60 seconds elapsed.")
        time.sleep(1)
    logger.info("Sleep test script finished normally after 60 seconds.")
except KeyboardInterrupt:
    logger.info("Sleep test script interrupted by user (Ctrl+C).")
except Exception as e:
    logger.error(f"Sleep test script encountered an error: {e}")
finally:
    logger.info("Exiting sleep test script.")
