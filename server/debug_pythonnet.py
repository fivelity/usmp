import logging
import sys
import traceback

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_pythonnet_detailed():
    """Test basic Python.NET functionality with detailed error reporting"""
    try:
        logger.info("1. Testing basic Python.NET import...")
        import pythonnet
        
        logger.info(f"2. Python.NET version: {pythonnet.__version__}")
        logger.info(f"3. Python.NET path: {pythonnet.__file__}")
        
        try:
            logger.info("4. Testing clr_loader import...")
            import clr_loader
            logger.info(f"5. clr_loader version: {clr_loader.__version__}")
            logger.info(f"6. clr_loader path: {clr_loader.__file__}")
        except Exception as e:
            logger.error(f"ERROR in clr_loader import: {e}")
            logger.error(traceback.format_exc())
        
        try:
            logger.info("7. Testing pythonnet.load...")
            pythonnet.load("coreclr")
            logger.info("8. pythonnet.load successful")
        except Exception as e:
            logger.error(f"ERROR in pythonnet.load: {e}")
            logger.error(traceback.format_exc())
            
        try:
            logger.info("9. Testing clr import...")
            import clr
            logger.info("10. clr import successful")
        except Exception as e:
            logger.error(f"ERROR in clr import: {e}")
            logger.error(traceback.format_exc())
            
        return True
    except Exception as e:
        logger.error(f"MAIN ERROR in pythonnet test: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== Python.NET Detailed Debug Test ===")
    print(f"Python version: {sys.version}")
    test_pythonnet_detailed()
    print("=== Test Complete ===")
