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
from PIL import Image
import sys
import math

DEFAULT_FILE = "numbers.jpg"
DEFAULT_DIM  = 10

GLOBAL_THRESHOLD_LOW = 50
GLOBAL_THRESHOLD_MED = 125
GLOBAL_THRESHOLD_HIGH = 200

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
	pixels = workImage.load()
	width, height = workImage.size
	for x in range(0, width):
		for y in range(0, height):
			if pixels[x, y][0] > globalThresh:
				pixels[x, y] = (255, 255)
			else:
				pixels[x, y] = (0, 255)
	return workImage

def getPixelsInWindow(workImage, startX, startY, winDim):
	pixels = workImage.load()
	width, height = workImage.size
	window = []

	maxX = startX * winDim + winDim
	if maxX > width:
		maxX = width

	maxY = startY * winDim + winDim
	if maxY > width:
		maxY = width

	for x in range(startX, maxX):
		for y in range(startY, maxY):
			window.append(pixels[startX*winDim + x, startY*winDim + y])
	return window

# Obtine o copie a imaginii image, segmentata cu o valoare de
# threshold calculata pentru ferestre de winDim x winDim pixeli
def getAdaptiveThreshImg(image, winDim):
	workImage = image.copy()
	pixels = workImage.load()
	width, height = workImage.size
	# Numarul de ferestre ce se vor aplica pe orizontala/verticala
	horizWinNr = int(math.ceil( width / winDim ))
	vertWinNr = int(math.ceil( height / winDim ))
	for x in range(0, horizWinNr):
		for y in range(0, vertWinNr):
			# lista cu pixelii din fereastra x, y
			window = getPixelsInWindow(workImage, x, y, winDim)
	return

# Entrypoint
def main():
	# Incarcarea imaginii de intrare
	im = getInputImage()
	# Afisarea imaginii de intrare
	#im.show()
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
	# raw_input("[ENTER] pentru a continua...")
	# Obtine dimensiunea ferestrei
	winDim = getWindowDimension()
	# Afisarea imaginilor segmentate cu threshold adaptiv
	imAdapThresh = getAdaptiveThreshImg(im, winDim)

	return

main()