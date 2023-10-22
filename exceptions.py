class IncorrectPhone(Exception):
    pass


class IncorrectBirthday(Exception):
    pass


class FlagError(Exception):
    pass


class SearchError(Exception):
    
    def __init__(self, user_input):
        self.massage = f"There is no such info: '{user_input}'"
        super().__init__(self.massage)


class SearchArgumentCountError(Exception):
    pass