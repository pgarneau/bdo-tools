import cv2
import numpy as np

# Load the image
image = cv2.imread('test.png')

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([22, 100, 100])
upper_yellow = np.array([26, 255, 255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
isolated = cv2.bitwise_and(image, image, mask=mask)

# Convert the image to grayscale
gray = cv2.cvtColor(isolated, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Potential color isolation
# mask = cv2.inRange()

# Apply Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop over the contours and filter them based on size and aspect ratio
health_bars = []
for contour in contours:
    # Get the bounding box for the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Filter by size and aspect ratio
    # aspect_ratio = w / float(h)
    if w > 10 and h > 3 and h < 6:
        health_bars.append((x, y, w, h))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the result
cv2.imshow('Detected Health Bars', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
