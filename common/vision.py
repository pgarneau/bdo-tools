
import cv2 as cv
import numpy as np
import os


class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    base = 0
    alpha = 0
    method = None
    threshold = 0.0

    # constructor
    def __init__(self, name, threshold=0.96, method=cv.TM_SQDIFF_NORMED, base_path=None):
        self.name = name
        if base_path:
            path = os.path.join(base_path, f"{name}.png")
        else:
            path = f"./spells/{name}.png"
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.needle_img = cv.imread(path, cv.IMREAD_UNCHANGED)
        self.threshold = threshold

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        self.base = self.needle_img[:,:,0:3]
        self.alpha = self.needle_img[:,:,3]
        self.alpha = cv.merge([self.alpha,self.alpha,self.alpha])

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, debug_mode=None):
        # make a copy of the image
        image = haystack_img.copy()
        # run the OpenCV algorithm
        result = cv.matchTemplate(image, self.base, self.method, mask=self.alpha)
        # for x in result:
        #     print(x)

        # Get the all the positions from the match result that exceed our threshold
        # locations = np.where(result >= threshold)
        locations = np.where(1-result >= self.threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        #print(rectangles)

        points = []
        coordinates = []
        if len(rectangles):
            #print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the points
                points.append((center_x, center_y))
                coordinates.append((x, y, w, h))

                if debug_mode:
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(image, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
            if debug_mode:
                print("Found something")
                cv.imshow('Matches', image)
                # cv.waitKey(500)
                # cv.destroyAllWindows()
                # cv.waitKey(0)
                # cv.destroyAllWindows()

        # if debug_mode:
        #     cv.imshow('Matches', image)
        #     cv.waitKey(2000)
        #     cv.destroyAllWindows()

        return coordinates
    

def find_nearby_targets(img, debug=True):
    edges = cv.Canny(img, 100, 200)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Loop over the contours and filter them based on size and aspect ratio
    health_bars = []
    for contour in contours:
        # Get the bounding box for the contour
        x, y, w, h = cv.boundingRect(contour)
        
        # Filter by size and aspect ratio
        aspect_ratio = w / float(h)
        if w >= 20 and h >= 4 and h <= 6 and aspect_ratio > 6:
            health_bars.append((x, y, w, h))
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), lineType=cv.LINE_4, thickness=2)

    if debug:
        cv.imshow('Detected Health Bars', img)
        # cv.waitKey(0)
    
    print(health_bars)
    return len(health_bars)

def find_shards(img, debug=None):
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, black_mask = cv.threshold(gray_image, 5, 255, cv.THRESH_BINARY_INV)

    blurred = cv.GaussianBlur(black_mask, (15, 15), 2)
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, dp=1, minDist=1, param1=50, param2=15, minRadius=4, maxRadius=6)

    detected_circles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, radius = circle
            detected_circles.append((x, y, radius))
            if debug:
                # Draw the detected circles on the original image
                cv.circle(img, (x, y), radius, (0, 255, 0), 2)  # Green circle
                cv.circle(img, (x, y), 2, (0, 0, 255), 3)      # Center point
    
    # Display the result if requested
    if debug:
        cv.imshow("Detected Yellow Circles", img)
        cv.imshow("Blurred", blurred)

    # we're detecting empty shards so to find number of shards we subtract from 3
    return max(3 - len(detected_circles), 0)