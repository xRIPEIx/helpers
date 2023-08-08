import os
import json
import numpy as np
from shapely.geometry import Polygon

def convert_to_dota_format(points):
            # Calculate the average y-coordinate value for all points
            avg_y = sum([point[1] for point in points]) / 4

            # Divide the points into upper and lower halves
            upper_points = [point for point in points if point[1] < avg_y]
            lower_points = [point for point in points if point[1] >= avg_y]

            # Find the point with the smallest x-coordinate in the upper half
            upper_points.sort(key=lambda point: point[0])
            left_upper = upper_points[0]

            # Find the point with the largest x-coordinate in the lower half
            lower_points.sort(key=lambda point: point[0], reverse=True)
            right_lower = lower_points[0]

            # Find the remaining two points
            upper_points.remove(left_upper)
            right_upper = upper_points[0]
            lower_points.remove(right_lower)
            left_lower = lower_points[0]

            # Rearrange the points in the DOTA dataset label format
            dota_points = [left_upper, right_upper, right_lower, left_lower]

            return dota_points

# Input folder path and output folder path
input_folder = "/home/PaddleDetection/license_plate_dataset_v2/training_dataset/annotations"
output_folder = "license_plate_dataset_v2/training_dataset/labelTxt"
os.makedirs(output_folder, exist_ok=True)

# Traverse all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        input_file_path = os.path.join(input_folder, filename)
        re_filename = filename.split('.')[0] + '.txt'
        output_file_path = os.path.join(output_folder, f"{re_filename}")

        # Read the JSON annotation file
        with open(input_file_path, "r") as f:
            annotation_data = json.load(f)

        # Get image width and height
        image_width = annotation_data["imageWidth"]
        image_height = annotation_data["imageHeight"]

        with open(output_file_path, "w") as f:
            # Get all points and labels in the file
            for target in annotation_data["shapes"]:
                
                # Get polygon vertex coordinates and label
                points = target["points"]
                label = target["label"]
                difficult = 0

                # Create a Polygon object and get the minimum bounding rectangle
                polygon = Polygon(points)
                min_bounding_rect = polygon.minimum_rotated_rectangle
                rect_points = list(min_bounding_rect.exterior.coords)
                rect_points = rect_points[:4]
                
                # Specify the position of the four points (top-left, top-right, bottom-right, bottom-left)
                rect_points = convert_to_dota_format(rect_points)
                coordinate = ""
                for x in range (4):
                    for i in range (2):
                        coordinate = coordinate + str(rect_points[x][i]) + " "
                    
                # Write the result to the new annotation file
                f.write(f'{coordinate}{label} {difficult}')
                f.write('\n')
