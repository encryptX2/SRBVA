"Proiect SRBVA" 

1. Python 2.7.13:
 https://www.python.org/downloads/

2. Python Image Library (PIL)
 Link-ul pentru Python 2.7 de pe pagina asta:
 http://www.pythonware.com/products/pil/

3. Eclipse Neon / Mars 2 testate de mine merg cu
 https://marketplace.eclipse.org/content/pydev-python-ide-eclipse
 daca vreti debugger (breakpoints and stuff) daca nu, orice editor text

Idei de continuare: sa mai adaugam o metoda de threshold adaptiv, momentan e doar 1 singura cu o fereastra in care valoarea de threshold se aplica ca medie a intensitatilor pixelilor, aici cateva alte metode din care putem alege:
http://homepages.inf.ed.ac.uk/rbf/HIPR2/adpthrsh.htm

Daca mai facem o metoda tot cu fereastra, in care valoarea de threshold sa se aleaga altfel + o metoda in care sa nu se foloseasca fereastra ci pixelii vecini, cred ca deja suntem barosani.
