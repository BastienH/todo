import cv2
import os

method = cv2.TM_SQDIFF_NORMED

large_image = "screenshots/20-Mar-19/20-Mar-19_Thu_13-24-00.png"
large_image = "screenshots/20-Mar-20_Fri_10-40-00.png"
small_image = "applications_data/identifiers/genergy title.png"
small_image = "applications_data/identifiers/genergy title long.png"

def find_img_in_img(small_image, large_image):
    # Read the images from the file
    small_image = cv2.imread(small_image)
    large_image = cv2.imread(large_image)

    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

    #Step 4 (Optional) : Crop the large_image

    # Display the original image with the rectangle around the match.
    cv2.imshow("output", large_image)

    # The image is only displayed if we call this
    cv2.waitKey(0)

for image in os.listdir("screenshots/20-Mar-19"):
    image = f"screenshots/20-Mar-19/{image}"
    find_img_in_img(small_image, image)
