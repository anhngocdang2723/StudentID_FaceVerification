import cv2
import numpy as np
import math

def rotate_image_horizontally(image, corners):
    """
    Rotates the image horizontally based on the four corners of the rectangle.

    :param image: The input image (numpy array).
    :param corners: A list of 4 tuples [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                    representing the corners of the rectangle.
    :return: The rotated image.
    """
    # Extract corners
    (x1, y1), (x2, y2), _, _ = corners

    # Calculate the angle with the horizontal
    delta_y = y2 - y1
    delta_x = x2 - x1
    angle = math.degrees(math.atan2(delta_y, delta_x))

    # Get image dimensions
    h, w = image.shape[:2]

    # Calculate the rotation matrix
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)

    # Rotate the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))

    return rotated_image

# Example usage
if __name__ == "__main__":
    # Load the image
    img = cv2.imread('rectangular_image.jpg')

    # Define the corners (example coordinates)
    corners = [(100, 150), (300, 130), (320, 300), (120, 320)]

    # Rotate the image
    rotated_img = rotate_image_horizontally(img, corners)

    # Show the results
    cv2.imshow("Original Image", img)
    cv2.imshow("Rotated Image", rotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
