class tampil:
    def __init__(self, tipe, skor, box):
        self.tipe = tipe
        self.skor = skor
        self.box = box

    def infodata(self):
        return f"tipe {self.tipe} skor {self.skor} box {self.box}"

