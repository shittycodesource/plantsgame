from settings.paths import SCORE_PATH, read_txt, write_txt

class Score:
    def __init__(self):
        self.value = 0
        self.setup()


    def setup(self):
        value = int(self.read_score())
        self.value = value


    def nullify(self):
        self.value = nullify


    def increase(self, n):
        self.value += n


    def decrease(self, n):
        if (self.value - n >= 0):
            self.value -= n


    def get_score(self):
        return self.value


    def read_score(self):
        value = int(read_txt(SCORE_PATH))
        print("Current score in file: ", value)
        return value


    def write_score(self):
        write_txt(SCORE_PATH, self.value)    
    
