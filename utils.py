#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Este archivo provee de funciones básicas que son globalmente usadas
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías de entorno
import errors


# Importación de librerías de sistema
try:
    from datetime import date
    from random import choice
    from urllib import urlencode
    from urllib2 import urlopen, Request
    import ctypes
    import os
    import string
    import time
except:
    errors.throw(errors.ERROR_IMPORTSYSTEMERROR)

# Constantes
_CMD_COLORS = {"blue":0x10,
              "gray":0x80,
              "green":0x20,
              "lblue":0x90,
              "lgray":0x70,
              "lgreen":0xA0,
              "lred":0xC0,
              "purple":0x50,
              "white":0xF0,
              "yellow":0x60,
              "lpurple":0xD0,
              "lyellow":0xE0,
              "red":0x40
}
_CONSOLE_WRAP = -25
_MSG_LOADINGFILE = "Cargando archivo '{0}' ..."
_MSG_OK = "[OK]"

# Se compara entre dos versiones y se retorna el ganador
def compareVersion(ver1, ver2):
    ver1 = ver1.split(".")
    ver2 = ver2.split(".")
    ganador = 0
    for i in range(3):
        if int(ver1[i]) > int(ver2[i]): return 1
        elif int(ver1[i]) < int(ver2[i]): return 2
    return 0

# Función que imprime un mensaje con un color
def colorcmd(cmd, color):
    if color in _CMD_COLORS:
        color = _CMD_COLORS[color]
        try:
            ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), color)
        except:
            pass
        print cmd,
        try:
            ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x07)
        except:
            pass
    else: print cmd,

# Elimina los acentos de un string
def delAccent(txt):
    txt = txt.replace("�?", "A").replace("É", "E").replace("�?", "I").replace("Ó", "O").replace("Ú", "U")
    return txt.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

# Borrar una matriz
def delMatrix(matrix):
    a = len(matrix)
    if a > 0:
        for k in range(a): matrix.pop(0)

# Limpia la pantalla
def clrscr():
    WConio.clrscr()

# Destruye el proceso del programa
def destroyProcess():
    os.system("taskkill /PID " + str(os.getpid()) + " /F")
    exit()

# Genera un string de 6 carácteres aleatorios
def generateRandom6():
    return ''.join(choice(string.ascii_uppercase) for i in range(6))

# Genera un string de 12 carácteres aleatorios
def generateRandom12():
    return ''.join(choice(string.ascii_uppercase) for i in range(12))

# Función que retorna un valor entre dos tagss
def getBetweenTags(html, tagi, tagf):
    tagi = tagi.strip()
    tagf = tagf.strip()
    try:
        posi = html.index(tagi)
        if ("<" in tagi) and (">" not in tagi):
            c = 1
            while True:
                try:
                    if html[posi + c] == ">":posi += (c + 1); break
                    c += 1
                except: return errors.ERROR_TAG_INITNOTCORRECTENDING
        else: posi += len(tagi)
        posf = html.index(tagf, posi)
        return html[posi:posf]
    except: return False

# Función que retorna la hora de sistema
def getHour():
    return time.ctime(time.time())[11:16]

# Obtiene la fecha del dia actual
def getDate():
    fecha = date.today()
    return str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)

# Devuelve el tamaño de la consola
def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except: return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except: pass
    if not cr: cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

# Obtener la versión del programa
def getVersion(label, headers):
    http_headers = {"User-Agent":headers}
    request_object = Request(LINK_PPPRJ, None, http_headers)
    response = urllib2.urlopen(request_object)
    html = response.read()
    html = getBetweenTags(getBetweenTags(html, "<" + label + ">", "</" + label + ">"), "<version>", "</version>")
    return html.strip()

# Traduce una linea usando el motor de traducciones de google
def googleTranslate(text, translate_lang, header, web, source_lang=None):
    if source_lang == None: source_lang = 'auto'
    params = urlencode({'client':'t', 'tl':translate_lang, 'q':text.encode('utf-8'), 'sl':source_lang})
    http_headers = {"User-Agent":header}
    request_object = Request(web + params, None, http_headers)
    response = urlopen(request_object)
    string = re.sub(',,,|,,', ',"0",', response.read())
    n = json.loads(string)
    translate_text = n[0][0][0]
    res_source_lang = n[2]
    return translate_text

# Función que comprueba si un elemento esta en una matriz (no completamente)
def isIn(termino, matriz):
    if termino != None:
        for elem in matriz:
            if elem in termino: return True
    return False

# Carga un archivo y retorna una matriz
def loadFile(archive, lang=_MSG_LOADINGFILE, **kwargs):
    if kwargs.get("show_state"): print lang.format("(...)" + archive[_CONSOLE_WRAP:].replace("//", "/")).replace("\"", ""),
    try:
        l = list()
        archive = open(archive, "r")
        for i in archive:
            l.append(i.decode('utf-8').strip())
        archive.close()
        if kwargs.get("show_state"): print _MSG_OK
    except:
        if kwargs.get("show_state"): print "error"
        l = []
    return l

# Función que imprime una matriz en pantalla
def printMatrix(matrix):
    for j in matrix:
        for k in j: print k,
        print "\n"

# Función que elimina datos repetidos
def sortAndUniq(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    output.sort()
    return output

# Función que divide un string en una lista usando un separador
def string2list(string, separator):
    return string.strip().split(separator)

# Función que suma lista de listas
def sumMatrix(matrix):
    suma = 0
    try:
        for j in matrix:
            for k in j: suma += k
        return suma
    except: return -1

# Test
if __name__ == '__main__':
    print string2list("foo bar", " ")
    print getDate()
    print getHour()
    colorcmd("test in purple\n", "purple")
    generateRandom6()
    print getTerminalSize()
    print loadFile("__init__.ini")
    print sortAndUniq([1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 10, 5])
    print getBetweenTags("<player>Username<title></title></player>", "<player>", "</player>")
    print getBetweenTags("<player>Username</player><title>Altername</title>", "<player>", "</player>")
    print getBetweenTags("<player>Username</player><title>Altername</title>", "<title>", "</title>")
