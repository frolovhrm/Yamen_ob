

base_name = 'yamen_ob.db'
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
screenshot_path = 'C:\\Python projects\\Screenshort\\'


class ScreenRead:
    def __int__(self):
        self.name = ''
        self.usable = 1
        self.readed = 0
        self.error_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Сохраняем код ошибки при заспознавании данных
        """ Разряды лога 0 - версия парсера
                    1 - activ
                    2 - rait
                    3 - grate
                    4 - all_profit
                    5 - cash_profit
                    6 - card_profit
                    7 - orders
                    8 - commission
                    9 - balance
                    10 - error function getFloat 
                    11 - tips """





