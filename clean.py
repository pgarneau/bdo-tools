
import cv2
import numpy as np

# Load the image
image = cv2.imread('clean_3.png')
template = cv2.imread('spells/nova/swooping.png', cv2.IMREAD_UNCHANGED)
template_base = template[:,:,0:3]
template_alpha = template[:,:,3]
template_alpha = cv2.merge([template_alpha, template_alpha, template_alpha])

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
v_channel = hsv[:, :, 2]

_, mask = cv2.threshold(v_channel, 220, 255, cv2.THRESH_BINARY)

# # _, mask = cv2.threshold(image, 230, 255, cv2.THRESH_BINARY)
# # mask = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

inpainted_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

result = cv2.matchTemplate(image, template_base, cv2.TM_SQDIFF_NORMED, mask=template_alpha)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(min_val)

# Draw rectangle around the matched region
h, w, _= template.shape
top_left = min_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(image, top_left, bottom_right, 255, 2)

# Show the result
cv2.imshow('Matched Result', image)
cv2.imshow('treated image', inpainted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()