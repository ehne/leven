from JMSSGraphics import *
import leven as leven
screenWidth = 800
screenHeight = 600


g = Graphics(width=screenWidth, height=screenHeight, fps=60)

class Rectangle:
    def __init__(self,x,y,w,h,colour, animationType):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        self.animationType = animationType
        self.animation = leven.Tweener({
            "start":{
                "v":["w"],
                "sv":[w],
                "ev":[700],
                "a":[animationType],
                "t":140,
                "->":"end"
            }
        },self)
        self.animation.start()
    def draw(self):
        g.drawRect(
            self.x,self.y,
            self.x+self.w,self.y+self.h,
            self.colour[0],self.colour[1],self.colour[2]
        )
    def update(self):
        self.animation.update()
        
listOfRects = []
for index, i in enumerate(leven.f):
    listOfRects.append(
        Rectangle(10,10+index*50,0,20,[1,1,1],i)
    )


@g.mainloop
def game():
    g.clear(0)

    for i in listOfRects:
        i.draw()
        i.update()
        g.drawText(f"{i.animationType} ↓",10,i.y+i.h,fontSize=14,fontName="JetBrains Mono")

g.run()