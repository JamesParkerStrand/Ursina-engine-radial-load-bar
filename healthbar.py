from ursina import *
from PIL import Image, ImageDraw

class RadialHealthBar():
    def __init__(self, thickness=10, col=(0, 100, 0), bar_color=(0, 255, 0), imageScale = 500):
        self.thickness = thickness
        self.col= col
        self.bar_color = bar_color
        self.imageScale = imageScale

        #the entity that displays the texture
        self.radial = Entity(model="plane",rotation_z=90,rotation_y=90, scale=6)

        #setup new image
        self.image = Image.new('RGBA', (self.imageScale, self.imageScale), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

        self.healthRatios = []

        for healthrange in range(0,101):

            ratioOfHealth = healthrange / 100
            healthConvertedToBar = ratioOfHealth * 360

            self.draw.ellipse((0, 0, self.imageScale - 1, self.imageScale -1), fill=self.col, width=1)
            self.draw.arc((0, 0, self.imageScale - 1, self.imageScale -1), 0, healthConvertedToBar, fill=self.bar_color, width=self.thickness)
            self.healthRatios.append( Texture(self.image) )

        del self.image, self.draw


        self.lastNumber = 0


        # call function, just to initialize the model's texture
        self.changeHealthOptimized(100, 100)

    def changeHealthOptimized(self, maxHealth, currentHealth):
        # get the health of the player, then convert that ratio into what can be used for referncing 0-100 frames of the health bar variants from the many health-ratios genrated
        ratioOfHealth = currentHealth / maxHealth
        healthConvertedToBar = ratioOfHealth * 100

        self.radial.texture = self.healthRatios[int(healthConvertedToBar)]


app = Ursina()

healthbar = RadialHealthBar(thickness=100)

cureentHealth = 100

def update():
    global cureentHealth
    cureentHealth -= 10*time.dt

    if cureentHealth <= 0:
        cureentHealth = 100
    healthbar.changeHealthOptimized(100, cureentHealth)


EditorCamera()

app.run()

