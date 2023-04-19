import cv2
import numpy as np

def seeded_region_growing(img, seed_point, threshold):
    """
    Implementation of seeded region growing algorithm for image segmentation.
    Args:
        img (numpy.ndarray): input image as numpy array.
        seed_point (tuple): a tuple of x, y coordinates of the seed point.
        threshold (float): threshold value for region growing.
    Returns:
        numpy.ndarray: segmented image as a binary numpy array.
    """
    # initialize segmented image with zeros
    segmented_img = np.zeros_like(img)

    # get the height and width of the image
    height, width = img.shape[:2]
 

    # initialize visited pixels with zeros
    visited = np.zeros_like(img)

    # initialize queue with seed point
    queue = []
    queue.append(seed_point)

    # loop through the queue until it is empty
    while queue:
        # get the current point from the queue
        current_point = queue.pop(0)

        # check if the current point is within the image bounds
        if current_point[0] < 0 or current_point[0] >= width or current_point[1] < 0 or current_point[1] >= height:
            continue

        # check if the current point has already been visited
        if visited[current_point[1], current_point[0]] == 1:
            continue

        # check if the difference between the current point and the seed point is less than the threshold
        #print(abs(img[current_point[1], current_point[0]] - img[seed_point[1], seed_point[0]]))
        if abs(img[current_point[1], current_point[0]] - img[seed_point[1], seed_point[0]]) < threshold:
            # add the current point to the segmented image
            segmented_img[current_point[1], current_point[0]] = 255

            # mark the current point as visited
            visited[current_point[1], current_point[0]] = 1

            # add the neighboring pixels to the queue
            queue.append((current_point[0]+1, current_point[1]))
            queue.append((current_point[0]-1, current_point[1]))
            queue.append((current_point[0], current_point[1]+1))
            queue.append((current_point[0], current_point[1]-1))

    return segmented_img

# load the image
img = cv2.imread('image.jpg', 0)

# set the seed point
seed_point = (100, 100)

# set the threshold value
threshold = 200

# perform seeded region growing segmentation
segmented_img = seeded_region_growing(img, seed_point, threshold)

# display the segmented image
cv2.imshow('Segmented Image', segmented_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
