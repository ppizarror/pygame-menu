#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Permite cargar configuraciones dado un archivo dado por parámetro
# Formato de archivo:
#
#    #comentario
#    CONFIG_1 = VALUE
#    CONFIG_2 = VALUE2
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import operator

import errors
from utils import string2list


# Definición de constantes
CONFIG_COMMENT = "#"
CONFIG_LOAD = "El archivo de configuraciones '{0}' ha sido cargado correctamente"
CONFIG_PRINTNOCONFIG = "No se encontraron configuraciones"
CONFIG_PRINTPARAM = "\t${0} : {1}"
CONFIG_PRINTPARAMETER = "Parametros cargados:"
CONFIG_PRINTPARAMSIMPLE = "\t{0}"
CONFIG_SAVED = "El archivo de configuraciones '{0}' ha sido guardado exitosamente"
CONFIG_SEPARATOR = " = "
FALSE = "FALSE"
TRUE = "TRUE"

# Carga configuraciones y retorna sus elementos
class configLoader:

    # Constructor, recibe un nombre de archivo como parámetro
    def __init__(self, filename, **kwargs):
        # Se carga el archivo de configuraciones
        try:
            file = open(filename, "r")
        except:
            errors.throw(errors.ERROR_NOCONFIGFILE, filename)
        # Variables
        self.config_single = []
        self.configs = {}
        self.filename = filename
        self.totalconfigs = 0
        # Se cargan las configuraciones
        for configline in file:
            if configline[0] != CONFIG_COMMENT and configline != "\n":
                config = string2list(configline, CONFIG_SEPARATOR)
                if len(config) == 1:
                    self.config_single.append(config[0])
                elif len(config) == 2:
                    self.totalconfigs += 1
                    self.configs[config[0]] = config[1]
                else:
                    errors.throw(errors.ERROR_BADCONFIG, configline, filename)
        if kwargs.get("verbose"):
            if not (self.totalconfigs + len(self.config_single)):
                errors.warning(errors.WARNING_NOCONFIGFOUND, filename)
            else:
                print CONFIG_LOAD.format(filename)
        file.close()

    # Función que exporta las configuraciones a un directorio
    def export(self, replace=True, name=None):
        if replace:
            name = self.filename
        f = open(name, "w")
        # Se escriben las configuraciones unarias
        for conf in self.config_single:
            f.write(str(conf) + "\n")
        # Se escriben las configuraciones complejas
        for key in self.configs.keys():
            f.write(str(key) + CONFIG_SEPARATOR + self.configs[key] + "\n")
        # Se cierra el archivo
        f.close()
        print CONFIG_SAVED.format(name)

    # Función que retorna true si el parámetro del archivo es verdadero
    def isTrue(self, param):
        if param in self.getParameters():
            if self.configs[param] == TRUE:
                return True
            else:
                return False
        else:
            errors.warning(errors.ERROR_CONFIGNOTEXISTENT, param)

    # Retorna una lista con todos los parametros cargados
    def getParameters(self):
        allconfigs = []
        for i in self.config_single:
            allconfigs.append(i)
        for j in self.configs.keys():
            allconfigs.append(j)
        return allconfigs

    # Retorna el valor del parametro param
    def getValue(self, param):
        if str(param).isdigit():
            param = int(param)
            if 0 <= param < len(self.config_single):
                return self.config_single[param]
            else:
                errors.throw(errors.ERROR_BADINDEXCONFIG, str(param))
        else:
            if param in self.getParameters():
                return self.configs[param]
            else:
                errors.warning(errors.ERROR_CONFIGNOTEXISTENT, param)

    # Imprime una lista con todos los parametros cargados
    def printParameters(self):
        if self.totalconfigs + len(self.config_single) > 0:
            print CONFIG_PRINTPARAMETER
            if self.totalconfigs > 0:
                for parameter in self.getParameters():
                    print CONFIG_PRINTPARAM.format(parameter, self.configs[parameter])
            for config in self.config_single:
                print CONFIG_PRINTPARAMSIMPLE.format(config)
        else:
            print CONFIG_PRINTNOCONFIG
        return

    # Define un parametro
    def setParameter(self, paramName, paramValue):
        self.configs[paramName] = paramValue

# Test
if __name__ == '__main__':
    binconfig = configLoader(".config\\bin.ini", verbose=True)
    binconfig.isTrue("DONT_WRITE_BYTECODE")
    binconfig.getParameters()
    binconfig.printParameters()
    binconfig.setParameter("PARAM1", "VALUE1")
    binconfig.setParameter("PARAM2", "VALUE2")
    binconfig.setParameter("PARAM3", "VALUE3")
    binconfig.setParameter("SET_DEFAULT_ENCODING", "W-850")
    binconfig.printParameters()
    binconfig.export(False, "hola.txt")
    print binconfig.getValue(binconfig.getParameters()[1])
    print binconfig.getValue("DONT_WRITE_BYTECODE")
    print binconfig.getValue("SET_DEFAULT_ENCODING")
