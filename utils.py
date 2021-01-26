import sys

def eprint(*args, **kwargs):
    """Prints errors to stderr"""
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(-1)
    
class WebDriverError(Exception):
    """Raised when webdriver is invalid
    
    Attributes:
        browser -- browser environment variable
    """
    
    def __init__(self, browser):
        self.message = f"Error: could not get webdriver for '{browser}'"
        super().__init__(self.message)

class PlatformError(Exception):
    """Raised when platform is invalid
    
    Attributes:
        platform -- platform environment variable
    """
    
    def __init__(self, platform):
        self.message = f"Error: this program cannot run on '{platform}'"
        super().__init__(self.message)