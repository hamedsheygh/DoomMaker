from direct.showbase.ShowBase import ShowBase
from panda3d.core import Texture, TextureStage, Plane, CardMaker, NodePath, Loader

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the texture
        texture = self.loader.loadTexture("brick.png")

        # Create a plane
        card_maker = CardMaker('plane')
        card_maker.setFrame(-1, 1, -1, 1)  # Setting the size of the plane
        plane = self.render.attachNewNode(card_maker.generate())

        # Apply texture to the plane
        plane.setTexture(texture, 1)

        # Position the camera so we can see the plane
        self.cam.setPos(0, -5, 0)
        self.cam.lookAt(0, 0, 0)

# Run the application
app = MyApp()
app.run()
