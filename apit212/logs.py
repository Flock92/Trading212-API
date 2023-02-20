from datetime import datetime

current = datetime.now().strftime('%H:%M:%S %d-%m-%Y')

class Log:
    def __init__(self):
        print("Error logged")
    def get_log(self, em):
        error_msg = self.msg
        log_msg=f"{error_msg}"
        return log_msg
