# =============================================================================
# base.py
# =============================================================================
# @AUTHOR: Yuxie Liu
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Class to be inherited
# =======================================================
class BaseController:
    """ Used as a base class for all controllers

        Used in other controllers as an inherited class to call super()
        to get some default parameters.
    """

    def __init__(self, tk_root, current_language, current_resolution):
        """ Initial method

            Args:
                tk_root: used to get the root tk window
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        self.tk_root = tk_root
        self.current_language = current_language
        self.current_controller = None # not always used, so not to be as default for each controller class
        self.current_resolution = current_resolution
