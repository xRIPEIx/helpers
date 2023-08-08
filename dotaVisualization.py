import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_image(points,image_path):

    plt.rcParams['figure.dpi'] = 300

    # Read the image
    image = plt.imread(image_path)

    # Create a new figure and draw the image
    plt.figure()
    plt.imshow(image)

    # Draw each polygon (rectangle)
    for points in polygons:
        polygon = plt.Polygon(points, edgecolor='blue', facecolor='none')
        plt.gca().add_patch(polygon)

        # Mark the vertices
        for x, y in points:
            plt.plot(x, y, 'blue', markersize=1)

    # Show the drawing
    plt.show()

polygons = [
        [(2764.705882352941, 2224.705882352941), (3120.508664153784, 2225.9997106503984), (3119.9999999999995, 2365.882352941176), (2764.1972181991564, 2364.5885246437188)],
        [(1509.6565832258316, 1986.2703637672548), (1704.2735042735046, 1957.2649572649573), (1718.548544979297, 2053.045875548985), (1523.931623931624, 2082.051282051282)]
    ]

image_path = "/home/PaddleDetection/license_plate_dataset_v2/training_dataset/images/IMG_082.jpg"

plot_image(polygons,image_path)
