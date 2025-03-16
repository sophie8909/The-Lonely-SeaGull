class BaseController:
    def __init__(self, tk_root, current_language, current_resolution):
        self.tk_root = tk_root
        self.current_language = current_language
        self.current_controller = None
        self.current_resolution = current_resolution


