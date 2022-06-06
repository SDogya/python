import sys
import numpy as np
from vispy import app, scene
from vispy.util.filter import gaussian_filter
from vispy.scene import visuals
canvas = scene.SceneCanvas(keys='interactive', bgcolor='black')
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='z', fov=60)

grid = visuals.GridLines()


view.add(grid)



z = np.random.normal(size=(550, 550), scale=200)
print(z)
z[100, 100] += 50000
z = gaussian_filter(z, (10, 10))

p1 = scene.visuals.SurfacePlot(z=z, color=(0.3, 0.3, 1, 1))
p1.transform = scene.transforms.MatrixTransform()
p1.transform.scale([1/249., 1/249., 1/249.])
view.add(p1)

# xax = scene.Axis(pos=[[0, 0], [1, 0]], tick_direction=(0, -1), axis_color='r', tick_color='r', text_color='r', font_size=16, parent=view.scene)
# yax = scene.Axis(pos=[[0, 0], [0, 1]], tick_direction=(-1, 0), axis_color='g', tick_color='g', text_color='g', font_size=16, parent=view.scene)
# zax = scene.Axis(pos=[[0, 0], [-1, 0]], tick_direction=(0, -1), axis_color='b', tick_color='b', text_color='b', font_size=16, parent=view.scene)
axis = visuals.XYZAxis(parent=view.scene)
# zax.transform = scene.transforms.MatrixTransform()  # its acutally an inverted xaxis
#
# zax.transform.rotate(90, (0, 1, 0))  # rotate cw around yaxis
# zax.transform.rotate(-45, (0, 0, 1))  # tick direction towards (-1,-1)

if __name__ == '__main__':
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()