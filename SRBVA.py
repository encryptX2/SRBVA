#####################################################################
# Proiect "Segmentarea prin threshold adaptiv"
# Aplicatia va realiza segmentarea unei imagini de intrare:
# 1. folosind 3 valori de threshold global (pentru a evidentia performantele thresholdului global).
# 2. folosind o fereastra de dimensiune dorita si doua tehnici
# 	 diferite pentru alegerea valorilor de treshhold in fereastra (prin media valorilor pixelilor 
# 	 din fereastra si prin metoda Otsu).
# 3. folosind un threshold calculat pentru fiecare pixel pe baza valorilor pixelilor din vecinatatea 
#    acestuia.
#
# Argumente permise:
# -f "Nume fisier" - numele fisierului ce va fi incarcat.
# 	Daca acest argument lipseste se va folosi fisierul DEFAULT_FILE
# 	Exemplu: segAdap.py -f "fisier.jpg"
#
# -d DIM_WIN - dimensiunea ferestrei de segmentare
# 	Daca acest argument lipseste se va folosi dimensiunea DEFAULT_DIM
# 	Exemplu: segAdap.py -d 15
#####################################################################
from __future__ import print_function

from Tkinter import *
import math
import sys

from PIL import Image, ImageTk
from pip._vendor.pkg_resources import working_set

# Parametrii default
DEFAULT_FILE = "numbers.jpg"
DEFAULT_DIM = 30

GLOBAL_THRESHOLD_LOW = 50
GLOBAL_THRESHOLD_MED = 125
GLOBAL_THRESHOLD_HIGH = 200

# Entrypoint
def main():
	# Incarcarea imaginii de intrare
	im = getInputImage()
	# Afisarea imaginii de intrare
	printProgress("Se afiseaza imaginea de intrare.")
	showImage("Imaginea initiala", im)
	
	# Afisarea imaginilor segmentate cu valoare globala
	printProgress("Segmentare cu threshold global = " + str(GLOBAL_THRESHOLD_LOW))
	imGTLow = getGlobalThreshImg(im, GLOBAL_THRESHOLD_LOW)
	showImage("Imaginea segmentata cu Threshold = " + str(GLOBAL_THRESHOLD_LOW), imGTLow)

	printProgress("Segmentare cu threshold global = " + str(GLOBAL_THRESHOLD_MED))
	imGTMed = getGlobalThreshImg(im, GLOBAL_THRESHOLD_MED)
	showImage("Imaginea segmentata cu Threshold = " + str(GLOBAL_THRESHOLD_MED), imGTMed)

	printProgress("Segmentare cu threshold global = " + str(GLOBAL_THRESHOLD_HIGH))
	imGTHigh = getGlobalThreshImg(im, GLOBAL_THRESHOLD_HIGH)
	showImage("Imaginea segmentata cu Threshold = " + str(GLOBAL_THRESHOLD_HIGH), imGTHigh)
	
	# Obtine dimensiunea ferestrei
	winDim = int(getWindowDimension())
	# Afisarea imaginilor segmentate cu threshold adaptiv calculat pe fereastra
	imAdapThresh, otsuAdapThresh = getAdaptiveThreshImgs(im, winDim)
	printProgress("Segmentare cu threshold adaptiv calculat per fereastra (prin medierea pixelilor)")
	showImage("Imaginea segmentata cu threshold adaptiv", imAdapThresh)
	
	printProgress("Segmentare cu threshold adaptiv calculat per fereastra (prin metoda Otsu)")
	showImage("Imaginea segmentata cu threshold prin metoda Otsu", otsuAdapThresh)
	
	# Imagine segmentata cu threshold calculat pe vecinatati de pixeli
	print("Se aplica metoda de calcul bazata pe vecinatati.")
	print("Calculul poate necesita o perioada mai mare de timp.")
	imVecinity = getAdaptiveVecinityImg(im, winDim)
	printProgress("Segmentare cu threshold adaptiv calculat pentru fiecare pixel din imagine")
	showImage("Imaginea segmentata cu threshold calculat per pixel", imVecinity)

	return

# Printeaza un mesaj dupa afisarea imaginilor
def printProgress(message):
	print(message)
	print("[Inchideti imaginea pentru a continua]")

# Obtine o imagine segmentata prin vecinatati de pixeli
def getAdaptiveVecinityImg(im, winDim):
	workImage = im.copy()
	pixels = workImage.load()
	width, height = workImage.size
	for x in range(width):
		for y in range(height):
			thresh = getVecinityThresh(x, y, im, winDim)
			if pixels[x, y][0] > thresh:
				pixels[x, y] = (255, 255)
			else:
				pixels[x, y] = (0, 255)
	return workImage

# Obtine valoarea de threshold pentru metoda bazata pe vecinatati
# Metoda presupune crearea unei ferestre de dimensiune winDim centrata
# pe pixelul pentru care se calculeaza valoarea de threshold si calculul mediei
# pixelilor din aceasta fereastra
def getVecinityThresh(crtX, crtY, im, winDim):
	pixels = im.load()
	width, height = im.size
	nrOfPixels, sumOfPixels = 0, 0
	# Limiteaza fereastra in care se va calcula thresholdul 
	# pentru a nu depasi marginile imaginii
	lowerX = crtX - (winDim /2)
	if( lowerX < 0 ): lowerX = 0
		
	higherX = crtX + (winDim / 2)
	if( higherX >= width ): higherX = width
	
	lowerY = crtY - (winDim /2)
	if( lowerY < 0 ): lowerY = 0
	
	higherY = crtY + (winDim / 2)
	if( higherY >= height ): higherY = height
	
	# Calculeaza suma valorilor pixelilor si numarul de pixeli din fereastra
	for x in range( lowerX, higherX ):
		for y in range( lowerY, higherY ):
			nrOfPixels += 1
			sumOfPixels += pixels[x, y][0]
	
	# Elimina din calcul pixelul pentru care se construieste thresholdul
	sumOfPixels -= pixels[crtX, crtY][0]
	nrOfPixels -= 1
	return sumOfPixels / nrOfPixels

# Afiseaza imaginea intr-o noua fereastra folosind titlul title
def showImage(title, img):
	width, height = img.size
	dispWindow = Tk()
	dispWindow.title(title)
	dispWindow.geometry(str(width + 100) + "x" + str(height + 30))
	
	p = ImageTk.PhotoImage(img)
	l = Label(dispWindow, image=p)
	l.image = p
	l.place(x=50, y=15)

	dispWindow.mainloop()
	return


# Functie utilitara pentru a gasi valori ale comenzilor -f, -d
def getArgVal(argCommand):
	for i in range(len(sys.argv)):
		if sys.argv[i] == argCommand:
			return sys.argv[i + 1]
	return

# Incarca imaginea specificata de argumentul de intrare
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


# Obtine limitele ferestrei window considerand dimensiunile imaginii workImage
def getMaxWinDimensions(workImage, window):
	width, height = workImage.size

	maxX = (window["winX"] + 1) * window["winDim"]
	if maxX > width:
		maxX = width

	maxY = (window["winY"] + 1) * window["winDim"]
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
	return int(math.floor(pixelSum / len(window)))

# Aplica valoarea thresh ferestrei
def applyThresholdToWindow(image, thresh, window):
	maxX, maxY = getMaxWinDimensions(image, window)
	thresholdImageArea(image, (window["winX"] * window["winDim"], window["winY"] * window["winDim"]), (maxX, maxY), thresh);
	return image

# Obtine o copie a imaginii image, segmentata cu o valoare de
# threshold calculata pentru ferestre de winDim x winDim pixeli
# folosind cele 2 metode de calcul ale valorii de threshold (medie + Otsu)
def getAdaptiveThreshImgs(image, winDim):
	meanImage = image.copy()
	otsuImage = image.copy()
	width, height = meanImage.size
	# Numarul de ferestre ce se vor aplica pe orizontala/verticala
	horizWinNr = int(math.ceil(width * 1.0 / winDim))
	vertWinNr = int(math.ceil(height * 1.0 / winDim))
	for x in range(0, horizWinNr):
		for y in range(0, vertWinNr):
			# lista cu pixelii din fereastra x, y
			window = {"winX" : x, "winY" : y, "winDim" : winDim}
			windowPixels = getPixelsInWindow(meanImage, window)
			thresh = getThresholdForWindow(windowPixels)
			applyThresholdToWindow(meanImage, thresh, window)
			
			otsuThresh = getOtsuThreshForWindow(windowPixels)
			applyThresholdToWindow(otsuImage, otsuThresh, window)
	
	return meanImage, otsuImage

# Obtine histograma imaginii definite de pixelii windowPixels
def histogram(windowPixels):
	size = len(windowPixels)
	hist = [0] * 256

	for px in range(size):
		# Pastreaza in vectorul hist numarul de aparitii ale 
		# fiecarei nuante de gri din vectorul de pixeli windowPixels
		gray_level = windowPixels[px][0]
		hist[gray_level] = hist[gray_level] + 1
	return hist

# Calculeaza valoarea de threshold a ferestrei ce contine pixelii 
# windowPixels prin metoda Otsu
# Aceasta metoda presupune impartirea pixelilor in 2 clase 
# (pixeli de fundal si pixeli de interes) pentru fiecare threshold posibil (0-255).
# Apoi, pentru fiecare clasa de pixeli se va calcula ponderea clasei in numarul total de pixeli.
# Folosind aceste ponderi cat si sumele pixelilor din fiecare clasa, se urmareste maximizarea 
# variatiei dintre cele 2 clase (delimitarea lor cat mai bine)
def getOtsuThreshForWindow(windowPixels):
	# Obtine histograma ferestrei de pixeli
	hist = histogram(windowPixels) 
	sumAll = 0
	# Calculeaza suma tuturor pixelilor din fereastra
	for t in range(256):
		sumAll += t * hist[t]
	
	# Defineste variabile pentru suma pixelilor de fundal, ponderea pixelilor de fundal, ponderea 
	# pixelilor de interes,  variatia maxima si valoarea de threshold
	sumBackPixels, weightBackPixels, weightFrontPixels, maxVariance, threshold = 0, 0, 0, 0, 0
	total = len(windowPixels)

	# Parcurge toate thresholdurile posibile
	for t in range(256):
		# Calculeaza ponderea pixelilor de fundal
		weightBackPixels += hist[t]
		if (weightBackPixels == 0): continue
		weightFrontPixels = total - weightBackPixels
		if (weightFrontPixels == 0) : break
		# Calculeaza media fiecarei clase de pixeli
		sumBackPixels += t * hist[t]
		meanBackPixels = sumBackPixels / weightBackPixels
		meanFrontPixels = (sumAll - sumBackPixels) / weightFrontPixels
		# Calculeaza variatia dintre clase
		inBetweenVariance = weightBackPixels * weightFrontPixels * (meanBackPixels - meanFrontPixels) ** 2 
		# Retine variatia maxima si valoarea de threshold aferenta acestei variatii
		if(inBetweenVariance > maxVariance):
			maxVariance = inBetweenVariance
			threshold = t

	return threshold

main()