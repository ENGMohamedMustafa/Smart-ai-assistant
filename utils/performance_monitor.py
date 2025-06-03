import time
import functools
import logging
from datetime import datetime
from typing import Callable, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def time_function(self, func_name: str = None):
        """Decorator to measure function execution time"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    result = None
                    success = False
                    logger.error(f"Function {func.__name__} failed: {e}")
                    raise
                finally:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    # Log performance
                    self._log_performance(
                        func_name or func.__name__,
                        execution_time,
                        success
                    )
                
                return result
            return wrapper
        return decorator
    
    def _log_performance(self, func_name: str, execution_time: float, success: bool):
        """Log performance metrics"""
        if func_name not in self.metrics:
            self.metrics[func_name] = {
                'total_calls': 0,
                'total_time': 0,
                'avg_time': 0,
                'successful_calls': 0,
                'failed_calls': 0
            }
        
        metrics = self.metrics[func_name]
        metrics['total_calls'] += 1
        metrics['total_time'] += execution_time
        metrics['avg_time'] = metrics['total_time'] / metrics['total_calls']
        
        if success:
            metrics['successful_calls'] += 1
        else:
            metrics['failed_calls'] += 1
        
        logger.info(f"{func_name}: {execution_time:.2f}s (Success: {success})")
    
    def get_metrics(self) -> dict:
        """Get performance metrics"""
        return self.metrics
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = {}

# Global performance monitor instance
monitor = PerformanceMonitor()