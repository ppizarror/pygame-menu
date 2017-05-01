#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Almacena todos los errores propios de bin, provee adem�s una función para retornar un
# mensaje de error dado parámetros

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Constantes de errores
ERROR_BADCONFIG = "La linea '{0}' del archivo de configuraciones '{1}' no es valida"
ERROR_BADINDEXCONFIG = "El indice seleccionado <{0}> no pertenece a las configuraciones cargadas"
ERROR_CANTTRANSLATE = "El texto no se puede traducir"
ERROR_CONFIGNOTEXISTENT = "El parametro <{0}> no existe en las configuraciones"
ERROR_HEADER = "Error :: "
ERROR_IMPORTERROREXTERNAL = "Ha ocurrido un error al importar las librerias de sistema externas"
ERROR_IMPORTERRORINTERNAL = "Ha ocurrido un error al importar las librerias internas de la aplicacion"
ERROR_IMPORTSYSTEMERROR = "Ha ocurrido un error al importar las librerias de sistema"
ERROR_LANGBADINDEX = "El indice <{0}> debe ser un numero entero mayor o igual a 10"
ERROR_LANGNOTEXIST = "ID[{0}] no existe en el archivo de idiomas <{1}>"
ERROR_NOCONFIGFILE = "No existe archivo de configuraciones '{0}'"
ERROR_NOLANGDEFINED = "El idioma no existe y/o no ha sido definido"
ERROR_NOLANGFILE = "No existe el archivo de idiomas '{0}'"
ERROR_NOTRANSLATECONECTION = "No se pudo establecer comunicacion con el servidor de traducciones"
ERROR_SCOREBOARD_BADPARAMETERS = "ERROR_BADPARAMETERS"
ERROR_SCOREBOARD_FAKEHASH = "ERROR_FAKEHASH"
ERROR_SCOREBOARD_FAKESCORE = "ERROR_FAKESCORE"
ERROR_SCOREBOARD_FAKETIME = "ERROR_FAKETIME"
ERROR_SCOREBOARD_FAKETRACK = "ERROR_FAKETRACK"
ERROR_SCOREBOARD_NOCONECTION = "ERROR_NO_CONECTION"
ERROR_SCOREBOARD_NOCONECTIONDB = "ERROR_NOCONECTION_DB"
ERROR_SCOREBOARD_NO_SCORES = "NO_SCORES"
ERROR_TAG_CANTRETRIEVEHTML = 16
ERROR_TAG_INITNOTCORRECTENDING = 14
ERROR_TAG_INITNOTFINDED = 13
ERROR_TAG_LASTNOTFINDED = 15
NO_ERROR = "OK"

WARNING_NOCONFIGFOUND = "No se han encontrado configuraciones en el archivo '{0}'"

# Función que crea un mensaje de error dado argumentos iniciales
def createMSG(message, *args):
    return message.format(*args)

# Función que termina el programa mostrando un mensaje de error
def throw(error, *args):
    print(ERROR_HEADER + createMSG(error, *args))
    exit()

# Función que imprime en pantalla un mensaje de error
def warning(error, *args):
    print ("Aviso :: " + createMSG(error, *args))
