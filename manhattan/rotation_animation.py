from manhattan import *

def rotateAnimate(points, n_frames = 100):
    points = [PolarPoint.fromEular(point) for point in points]
    for i in range(n_frames):
        print(i)
        plt.cla()
        scatter(points)
        plt.draw()
        plt.pause(.1)
        for point in points:
            point.theta += 2 * PI / n_frames

# rotateAnimate(circle(1, 50))
rotateAnimate(square(1, 200))
