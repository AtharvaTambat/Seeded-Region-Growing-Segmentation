from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy import ndimage
import random
import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image


class SeedSegment(object):
	def __init__(self,img_name,img,threshold, num_segments):
		self.gray_image = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
		self.stack=[]
		self.img=img
		self.height,self.width=np.shape(self.gray_image)
		self.image_label=np.full_like(self.img,0)
		self.k=num_segments
		self.threshold=threshold
		self.preprocess()

	def preprocess(self):
		'''Pre-process image by smoothening the image'''
		self.img = cv2.GaussianBlur(self.img,(3,3),sigmaX=2, sigmaY=2)

	def segment(self):
		'''Choose seed points using top-hat transform and run the main loop for image segmentation'''

		# Define structuring element for TopHat transform
		kernel_size = 25
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

		# Apply TopHat transform
		tophat = cv2.morphologyEx(self.gray_image, cv2.MORPH_TOPHAT, kernel)

		# Threshold TopHat transform output
		_, binary = cv2.threshold(tophat, 90, 255, cv2.THRESH_BINARY)

		# Apply morphological opening operation
		kernel_size = 5
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
		opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

		# Apply connected component labeling algorithm
		num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening)

		# Draw centroids on original image
		for centroid in centroids[1:]:
			cv2.circle(self.gray_image, (int(centroid[0]), int(centroid[1])), 5, (255, 0, 0), -1)

		# Display results
		cv2.imshow('Input Image', self.gray_image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		count = 0
		taken = []
		for i in range(len(centroids)):
			# index = int(np.random.randint(0,len(centroids)-1))
			index = i
			x=int(centroids[index][0])
			y=int(centroids[index][1])
			if self.check_within_img(x,y) and self.image_label[x,y]==0 and (x,y) not in taken:
				self.image_label[x,y]=count+1
				self.stack.append((x,y))
				taken.append((x,y))
				count+=1
			if count >= self.k:
				break

		# Grow the region
		while len(self.stack)!=0:
			x,y=self.stack.pop(0)
			self.grow(x,y)

		# Create segmented image with num_segment gray levels
		clustering={}
		cluster_count={}
		for i in range(self.k):
			clustering[i+1]=0
			cluster_count[i+1]=0
		for i in range(self.height):
			for j in range(self.width):
				if self.image_label[i,j]!=0:
					clustering[self.image_label[i,j]]+=self.img[i,j]
					cluster_count[self.image_label[i,j]]+=1
		for i in range(self.k):
			clustering[i+1]=clustering[i+1]/cluster_count[i+1]
		for i in range(self.height):
			for j in range(self.width):
				if self.image_label[i,j]==0:
					self.image_label[i,j]=self.nearest((i,j),clustering)


	def nearest(self,point,clustering):
		'''To find the nearest neighbor, if the pixel is left unlabelled, and classify the pixel in nearest class'''
		x,y=point
		a=[]
		for i in range(self.k):
			a.append(abs(self.img[x,y]-clustering[i+1]))
		return 1+a.index(min(a))


	def neighbour(self,x1,y1):
		'''Return 8-neighbour of the pixel (x1,y1)'''
		neighbour=[]
		for i in (-1,0,1):
			for j in (-1,0,1):
				if i==0 and j==0:
					continue
				x=x1+i
				y=y1+j
				if self.check_within_img(x,y):
					neighbour.append((x,y))
		return neighbour

	def check_within_img(self,x,y):
		'''Checks whether the pixel is in image bounds'''
		return True if 0<=x<self.height and 0<=y<self.width else False


	def grow(self,x1,y1):
		'''Choose neighbours of a pixel based on the threshold'''
		curr_label=self.image_label[x1,y1]
		for x,y in self.neighbour(x1,y1):
			# print(x,y)
			if self.image_label[x,y]==0:
				if abs(self.img[x,y]-self.img[x1,y1])<=self.threshold:
					self.image_label[x,y]=curr_label
					self.stack.append((x,y))
			
	def result(self):
		'''Create segmented image'''
		temp={}
		val=0
		cluster_count=0
		clustering={}
		val1=int(255/self.k)
		for i in range(self.k-1):
			temp[i+1]=val
			val=val+val1
			clustering[i+1]=0
		temp[self.k]=255
		clustering[self.k]=0
		for i in range(self.height):
			for j in range(self.width):
				if self.image_label[i,j]==0:
					cluster_count+=1
				else:
					self.img[i,j]=temp[self.image_label[i,j]]
					clustering[self.image_label[i,j]]+=1

def browse_image_file():
    image_file = filedialog.askopenfilename(title="Select an image file")
    image_file_entry.delete(0, tk.END)
    image_file_entry.insert(0, image_file)

def browse_output_dir():
    output_dir = filedialog.askdirectory(title="Select an output directory")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)

def process_image():
    # Get the values of the input image file and output directory
    image_file = image_file_entry.get()
    output_dir = output_dir_entry.get()
    output_file_name = output_file_entry.get()
    threshold = int(threshold_entry.get())
    num_segments = int(segments_entry.get())

    try:
		# Perform image segmentation
        with Image.open(image_file) as image:
            Image1 = cv2.imread(image_file)
            r, g, b = Image1[:,:,0], Image1[:,:,1], Image1[:,:,2]
            gray_img = 0.2989 * r + 0.5870 * g + 0.1140 * b
            SRG=SeedSegment(image_file, gray_img, threshold, num_segments)
            SRG.segment()
            SRG.result()

			# Save the segmented image to the output directory
            output_path = output_dir + '/' + output_file_name
            cv2.imwrite(output_path,SRG.img)


		# Display a success message box
        messagebox.showinfo("Image Segmentation", "Image segmented and saved successfully!")
	
    except Exception as e:
		# Display an error message box if image processing fails
        messagebox.showerror("Image Segmentation", "Error processing image: " + str(e))

# Create the main window
window = tk.Tk()
window.title("Image Processing App")

# Create a frame for the input controls
input_frame = tk.Frame(window, padx=10, pady=10)
input_frame.pack(fill="both", expand=True)

# Create a label and entry for the input image file
image_file_label = tk.Label(input_frame, text="Input Image File:")
image_file_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 5))
image_file_entry = tk.Entry(input_frame, width=50)
image_file_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 5))
browse_image_button = tk.Button(input_frame, text="Browse", command=browse_image_file)
browse_image_button.grid(row=0, column=3, sticky="e", pady=(0, 5))

# Create a label and entry for the output directory
output_dir_label = tk.Label(input_frame, text="Output Directory:")
output_dir_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 5))
output_dir_entry = tk.Entry(input_frame, width=50)
output_dir_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(0, 5))
browse_output_button = tk.Button(input_frame, text="Browse", command=browse_output_dir)
browse_output_button.grid(row=1, column=3, sticky="e", pady=(0, 5))

# Create a label for the output file name
output_file_label = tk.Label(input_frame, text="Output File Name:")
output_file_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 5))

# Create an entry box for the output file name
output_file_entry = tk.Entry(input_frame, width=50)
output_file_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(0, 5))

# Create a label for the threshold input
threshold_label = tk.Label(input_frame, text="Threshold:")
threshold_label.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 5))

# Create an entry box for the threshold input
threshold_entry = tk.Entry(input_frame)
threshold_entry.grid(row=3, column=1, sticky="w", pady=(0, 5))

# Create a label for the number of segments input
segments_label = tk.Label(input_frame, text="Number of segments:")
segments_label.grid(row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 5))

# Create an entry box for the number of segments input
segments_entry = tk.Entry(input_frame)
segments_entry.grid(row=4, column=1, sticky="w", pady=(0, 5))

# Create a button to start the image processing
process_button = tk.Button(input_frame, text="Process Image", command=process_image)
process_button.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(10, 0))

# Start the main event loop
window.mainloop()

