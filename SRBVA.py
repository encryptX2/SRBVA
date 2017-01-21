#####################################################################
# Proiect "Segmentarea prin threshold adaptiv"
# Aplicatia va realiza segmentarea unei imagini de intrare:
# 1. folosind 3 valori de threshold global
# 2. folosind o fereastra de dimensiune dorita si doua tehnici
# diferite pentru alegerea valorilor de treshhold.
#
# Argumente permise:
# -f "Nume fisier" - numele fisierului ce va fi incarcat.
#	Daca acest argument lipseste se va folosi fisierul DEFAULT_FILE
#	Exemplu: seg_adap.py -f "fisier.jpg"
#
# -d DIM_WIN - dimensiunea ferestrei de segmentare
#	Daca acest argument lipseste se va folosi dimensiunea DEFAULT_DIM
#	Exemplu: seg_adap.py -d 15
#####################################################################
from __future__ import print_function
from Tkinter import *
from PIL import Image, ImageTk
import sys
import math

DEFAULT_FILE = "numbers.jpg"
DEFAULT_DIM  = 15

GLOBAL_THRESHOLD_LOW = 50
GLOBAL_THRESHOLD_MED = 125
GLOBAL_THRESHOLD_HIGH = 200

# Entrypoint
def main():
	# Incarcarea imaginii de intrare
	im = getInputImage()
	# Afisarea imaginii de intrare
	#im.show()
	showImage("Imaginea initiala", im)
	# Afisarea imaginilor segmentate cu valoare globala
	# raw_input("[ENTER] pentru a continua...")
	# print("Segmentare cu threshold global = " + str(GLOBAL_THRESHOLD_LOW))
	# imGTLow = getGlobalThreshImg(im, GLOBAL_THRESHOLD_LOW)
	# imGTLow.show()
	# raw_input("[ENTER] pentru a continua...")
	# print("Segmentare cu threshold global = " + str(GLOBAL_THRESHOLD_MED))
	# imGTMed = getGlobalThreshImg(im, GLOBAL_THRESHOLD_MED)
	# imGTMed.show()
	# raw_input("[ENTER] pentru a continua...")
	# print("Segmentare cu threshold global = " + str(GLOBAL_THRESHOLD_HIGH))
	# imGTHigh = getGlobalThreshImg(im, GLOBAL_THRESHOLD_HIGH)
	# imGTHigh.show()
	#raw_input("[ENTER] pentru a continua...")
	# Obtine dimensiunea ferestrei
	winDim = int( getWindowDimension() )
	# Afisarea imaginilor segmentate cu threshold adaptiv
	imAdapThresh = getAdaptiveThreshImg(im, winDim)
	showImage("Imaginea segmentata cu threshold adaptiv", imAdapThresh)
	#imAdapThresh.show()
	
	imHistogram = histogram(im)
	print(imHistogram)
	
	raw_input("[ENTER] pentru a continua...")
	threshold = otsu_thrd(im)
	print(threshold)
	
	raw_input("[ENTER] pentru a continua...")
	otsuIm = segment(im, threshold)
	otsuIm.show()
	
	
	
	return

# Afiseaza imaginea intr-o noua fereastra
def showImage(title, img):
	width, height = img.size
	dispWindow = Tk()
	dispWindow.title(title)
	dispWindow.geometry(str(width + 100) + "x" + str(height + 30))
	
	p = ImageTk.PhotoImage(img)
	l = Label(dispWindow, image = p)
	l.image = p
	l.place(x=50,y=15)

	dispWindow.mainloop()
	return


# Functie utilitara pentru a gasi valori ale comenzilor -f, -d
def getArgVal(argCommand):
	for i in range(len(sys.argv)):
		if sys.argv[i] == argCommand:
			return sys.argv[i +1]
	return

# Incarca fisierul specificat de argumentele de intrare
# sau fisierul default
def getInputImage():
	fileName = getArgVal("-f")
	if fileName is None:
		fileName = DEFAULT_FILE

	return Image.open(fileName).convert('LA')

# Obtine dimensiunea ferestrei folosite la segmentare
def getWindowDimension():
	dim = getArgVal("-d")
	if dim is None:
		dim = DEFAULT_DIM
	return dim

# Obtine o copie a imaginii image, segmentata cu valoarea globalThresh
def getGlobalThreshImg(image, globalThresh):
	workImage = image.copy()
	width, height = workImage.size
	
	return thresholdImageArea(workImage, (0, 0), (width, height), globalThresh)

# Segmenteaza imaginea image intre startPoint si endPoint cu valoarea threshValue
def thresholdImageArea(image, startPoint, endPoint, threshValue):
	pixels = image.load()
	for x in range(startPoint[0], endPoint[0]):
		for y in range(startPoint[1], endPoint[1]):
			if pixels[x, y][0] >= threshValue:
				pixels[x, y] = (255, 255)
			else:
				pixels[x, y] = (0, 255)
	return image


def getMaxWinDimensions(workImage, window):
	width, height = workImage.size

	maxX = (window["winX"] +1) * window["winDim"]
	if maxX > width:
		maxX = width

	maxY = (window["winY"] +1) * window["winDim"]
	if maxY > height:
		maxY = height
	return maxX, maxY

# Obtine toti pixelii din fereastra window
def getPixelsInWindow(workImage, window):
	pixels = workImage.load()
	# limiteaza valorile maxime pe axele x si y 
	# pentru a nu depasi dimensiunea imaginii
	maxX, maxY = getMaxWinDimensions(workImage, window)
	
	windowPixels = []

	# Obtine pixelii aflati intre pozitiile: winX * winDim si maxX pe x
	# si  winY * winDim si maxY pe y
	for x in range(window["winX"] * window["winDim"], maxX):
		for y in range(window["winY"] * window["winDim"], maxY):
			windowPixels.append(pixels[ x, y])
	return windowPixels

# Obtine valoarea thresholdului ce va fi aplicat ferestrei
# Metoda de obtinere a thresholdului folosind media pixelilor
def getThresholdForWindow(window):
	pixelSum = 0
	for i in range(len(window)):
		pixelSum += window[i][0]
	return int( math.floor( pixelSum / len(window) ) )

# Aplica valoarea thresh ferestrei
def applyThresholdToWindow(image, thresh, window):
	maxX, maxY = getMaxWinDimensions(image, window)
	thresholdImageArea(image, (window["winX"] * window["winDim"], window["winY"] * window["winDim"]), (maxX, maxY), thresh);
	return image

# Obtine o copie a imaginii image, segmentata cu o valoare de
# threshold calculata pentru ferestre de winDim x winDim pixeli
def getAdaptiveThreshImg(image, winDim):
	workImage = image.copy()
	width, height = workImage.size
	# Numarul de ferestre ce se vor aplica pe orizontala/verticala
	horizWinNr = int(math.ceil( width *1.0 / winDim ))
	vertWinNr = int(math.ceil( height *1.0 / winDim ))
	for x in range(0, horizWinNr):
		for y in range(0, vertWinNr):
			# lista cu pixelii din fereastra x, y
			window = {"winX" : x, "winY" : y, "winDim" : winDim}
			windowPixels = getPixelsInWindow(workImage, window)
			thresh = getThresholdForWindow( windowPixels )
			applyThresholdToWindow(workImage, thresh, window)
			# TODO : foloseste fereastra pentru a calcula thresholdul
			# si aplica-l pixelilor din fereastra
	return workImage

def histogram(image):
 	pix =image.load()
 	width, height = image.size
  	hist = [0]*256

  	for y in range(height):
   	 	for x in range(width):
  	   		gray_level= pix[x, y][0]
  	  	  	hist[gray_level] = hist[gray_level]+1
  	return hist

def otsu_thrd(image):
	#prima data luam datele din histograma 
 	hist = histogram(image) 
  	sum_all = 0
  	width, height = image.size
   	# sum the values of all background pixels
   	for t in range(256):
 	   sum_all += t * hist[t]
  	sum_back, w_back, w_fore, var_max, threshold = 0, 0, 0, 0, 0
  	total = height*width 

 	# go over all possible thresholds
  	for t in range(256):
   		# update weights
   		hist_data = histogram(image)
   		w_back += hist_data[t]
 	   	if (w_back == 0): continue
  	   	w_fore = total - w_back
   	   	if (w_fore == 0) : break
    	# calculate classes means
		sum_back += t * hist_data[t]
 		mean_back = sum_back / w_back
  		mean_fore = (sum_all - sum_back) / w_fore
   		# Calculate Between Class Variance
    	var_between = w_back * w_fore * (mean_back - mean_fore)**2 
    	# a new maximum is found?
	if(var_between > var_max):
			var_max = var_between
			threshold = t

   	return threshold	
   
def segment(im, thrd = 128):
    width, height = im.size
    mat = im.load()
    out = Image.new('1',(width, height)) 
    out_pix = out.load()
    for x in range(width): # go over the image columns
 	   for y in range(height): # go over the image rows
 		if mat[x, y] >= thrd: # compare to threshold
  		   	out_pix[x, y] = 255
   		else:
   			out_pix[x, y] = 0
    return out  

main()