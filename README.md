# Seeded Region Growing Segmentation

## Description
The aim is to create an application for segmenting images using seeded region growing algorithm (with Tophat transform)

1. ```dataset``` - stores the entire dataset used for image segmentation
2. ```input``` - stores some sample inputs seected from the dataset
3. ```results``` - stores the sample result of running our seeded image growing algorithm on the sample input images
4. ```src``` - contains the executable (in the ```dist``` folder) and the python script used for creating the executable
5. ```img_segment``` - the executable file to run the program

## How to use?
1. Double click on the executable file named "img_segment" OR type ./img_segment on the terminal and wait for it to open
2. A window, like the one shown below will open. Choose the input file and the directory in which you would like your segmented image to be present

![App Usage](./app_usage_images/Screenshot%20from%202023-04-23%2012-37-38.png "App Usage")

3. Type in the name of your segmented image file (with an image extension - .png, .jpg etc.)
4. Enter the threshold parameter
5. Enter the number of segments which you speculate your image to have
5. Press "Process Image"
6. A window (like the one below) with the grayscale version of the image with bright spots at the locations of the seed points calculated using TopHat Transform is displayed

![App Usage](./app_usage_images/Screenshot%20from%202023-04-23%2012-42-34.png "App Usage")

7. Press 'ESC' to continue
8. A dialog box, indicating that the segmentation was successful will be displayed if it was successful, or an error dialog box will be shown.

![App Usage](./app_usage_images/Screenshot%20from%202023-04-23%2012-45-42.png "App Usage")

9. Click "OK" and repeat as many times as you want, before exiting the window by clicking "X" on the top right corner of the window.

## Input parameters used for sample inputs

The parameters used to produce the results are given below (also mentioned in the name of the output images in the results folder)
1. ```img_part_001.jpg``` - Threshold: 4, Number of segments: 5
2. ```img_part_002.jpg``` - Threshold: 3, Number of segments: 5
3. ```img_part_003.jpg``` - Threshold: 3, Number of segments: 5
4. ```img_part_005.jpg``` - Threshold: 5, Number of segments: 5
5. ```img_part_006.jpg``` - Threshold: 2, Number of segments: 4
6. ```img_part_007.jpg``` - Threshold: 3, Number of segments: 5
7. ```img_part_008.jpg``` - Threshold: 3, Number of segments: 5


