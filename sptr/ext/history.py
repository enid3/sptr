class History:
    def __init__(self, maxlen=None):
        assert maxlen is not None, "maxlen can't be None"
        assert maxlen > 0, "maxlen must be >0"

        self.history = []
        self.maxlen = maxlen

    def add(self, item):
        if len(self.history) > self.maxlen - 1:
            del self.history[0]

        if self.history[-1] == item:
            del self.history[-1]

        self.history.append(item)
