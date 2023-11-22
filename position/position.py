class Position:
    def __init__(self, pixelsX, pixelsY):
        self.x = pixelsX
        self.y = pixelsY

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def addX(self, pixelsX):
        self.x += pixelsX

    def addY(self, pixelsY):
        self.y += pixelsY

    def setX(self, pixelsX):
        self.x = pixelsX

    def setY(self, pixelsY):
        self.y = pixelsY
        
    def updatePosition(self, pixelsX, pixelsY):
        self.addX(pixelsX)
        self.addY(pixelsY)

    def getPosition(self):
        return self.x, self.y