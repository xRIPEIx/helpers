import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

# List of COCO annotation data
annotations = [
    {
        "category_id": 1,
            "segmentation": [
                [
                    2764.705882352941,
                    2224.705882352941,
                    3120.508664153784,
                    2225.9997106503984,
                    3119.9999999999995,
                    2365.882352941176,
                    2764.1972181991564,
                    2364.5885246437188
                ]
            ],
            "iscrowd": 0,
            "bbox": [
                2942.35302734375,
                2295.2939453125,
                355.8050842285156,
                139.88348388671875,
                0.003636676964961394
            ],
            "area": 49771.25476649217,
            "image_id": 76,
            "id": 81
    },
    {
        "category_id": 1,
            "segmentation": [
                [
                    1509.6565832258316,
                    1986.2703637672548,
                    1704.2735042735046,
                    1957.2649572649573,
                    1718.548544979297,
                    2053.045875548985,
                    1523.931623931624,
                    2082.051282051282
                ]
            ],
            "iscrowd": 0,
            "bbox": [
                1614.1025390625,
                2019.658203125,
                196.7665252685547,
                96.83880615234375,
                -0.1479492406061561
            ],
            "area": 19054.635397751816,
            "image_id": 76,
            "id": 82
    }
]

# Load the image
image_path = "/home/PaddleDetection/license_plate_dataset_v2/training_dataset/images/IMG_082.jpg"
image = cv2.imread(image_path)

# Draw bounding boxes on the image
for annotation_data in annotations:
    x, y, width, height, angle = annotation_data["bbox"][:5]
    x, y, width, height, angle = int(x), int(y), int(width), int(height), float(angle)

    # Calculate the corners of the rotated bounding box
    rect = ((x, y), (width, height), angle*180/math.pi)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Draw the rotated bounding box on the image
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

# Show the image with all the rotated bounding boxes
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
