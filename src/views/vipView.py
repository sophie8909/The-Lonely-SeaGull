from views.customerView import CustomerView

class VIPView(CustomerView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)
        