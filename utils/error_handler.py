import logging
import traceback
from functools import wraps
from typing import Callable, Any
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ErrorHandler:
    @staticmethod
    def handle_api_error(func: Callable) -> Callable:
        """Decorator for handling API errors"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"API Error in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                logger.error(traceback.format_exc())
                
                # Show user-friendly error in Streamlit
                if hasattr(st, 'session_state'):
                    st.error(f"⚠️ Service temporarily unavailable. Please try again.")
                
                return None
        return wrapper
    
    @staticmethod
    def handle_file_error(func: Callable) -> Callable:
        """Decorator for handling file operation errors"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                error_msg = f"File not found in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                st.error("📁 File not found. Please check the file path.")
                return None
            except PermissionError as e:
                error_msg = f"Permission error in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                st.error("🔒 Permission denied. Please check file permissions.")
                return None
            except Exception as e:
                error_msg = f"File operation error in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                logger.error(traceback.format_exc())
                st.error("📄 File processing error. Please try again.")
                return None
        return wrapper
    
    @staticmethod
    def log_user_action(action: str, details: dict = None):
        """Log user actions for analytics"""
        log_data = {
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        logger.info(f"User Action: {log_data}")

# Global error handler instance
error_handler = ErrorHandler()