from enums import UserLanguage, ViewMode, ViewType, MeasureSystem

class AppView():
    def __init__(self, view_type):
        # defaults to english for ease of english-speaking software developers
        self.language = UserLanguage.ENGLISH
        self.view_mode = ViewMode.DARK
        if type(view_type) == ViewType:
            self.view_type = view_type
        else:
            self.view_type = ViewType.CUSTOMER
        self.measure = MeasureSystem.METRIC

