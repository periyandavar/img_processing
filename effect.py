#step 1
#Use bilateral filter for edge-aware smoothing.
import cv2
def fun(image):
 grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 #invert the gray image
 grayImageInv = 250 - grayImage 
 
 #Apply gaussian blur
 grayImageInv = cv2.GaussianBlur(grayImageInv, (21, 21), 0)
 
 #blend using color dodge
 output = cv2.divide(grayImage, 255-grayImageInv, scale=256.0)
 
 #create windows to dsiplay images

 return output 
def cartoon(img):
 num_down = 2 # number of downsampling steps
 num_bilateral = 7 # number of bilateral filtering steps
 
 img_rgb = img
 
 # downsample image using Gaussian, pyramid
 img_color = img_rgb
 for _ in range(num_down):
   img_color = cv2.pyrDown(img_color)
 
 # repeatedly apply small bilateral filter instead of
 # applying one large filter
 for _ in range(num_bilateral):
  img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)
 
 # upsample image to original size
 for _ in range(num_down):
   img_color = cv2.pyrUp(img_color)
 
 #STEP 2 & 3
 #Use median filter to reduce noise
 # convert to grayscale and apply median blur
 img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
 img_blur = cv2.medianBlur(img_gray, 7)
 
 #STEP 4
 #Use adaptive thresholding to create an edge mask
 # detect and enhance edges
 img_edge = cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,blockSize=9,C=2)
 # Step 5
 # Combine color image with edge mask & display picture
 # convert back to color, bit-AND with color image
 img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
 height, width, channels = img_color.shape
 img_edge = cv2.resize(img_edge, (width,height), interpolation = cv2.INTER_AREA)
 img_cartoon = cv2.bitwise_and(img_color, img_edge)
 
 # display
 return(img_cartoon)
 
def bl_white(img):
	grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	  
	(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 255, cv2.THRESH_BINARY)
	return blackAndWhiteImage;

