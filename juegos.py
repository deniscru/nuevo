import hangman							#Uso la ESTRUCTURA DE DATOS DICCIONARIOS por que puedo guardar cualquier tipo de datos 
import reversegam						#y tambien poder acceder a estos datos de forma directa mediante una clave la cual 
import tictactoeModificado				#puedo asignarla, y haci poder guardar cada campo de los jugadores de una forma ordenada
import json
import PySimpleGUI as sg				#El archivo que utilizo es json porque este modulo puede almacenar diccionarios 
import os								#o listas sin realizar cambios la cual python tiene estructuras iguales, y haci 
										#se me hace facil a mi por que yo estoy usando diccionarios como estructura
def error(tipo):									#notifico los errores que me pueden salir
	error_nombre= [
				[sg.Text('ERROR!! el nombre ingresado ya existe')],
				[sg.Button('OK')]]
	error_datos= [
				[sg.Text('ERROR!! algunos de los campos no fue completado')],
				[sg.Button('OK')]]	
	error_opcion= [
				[sg.Text('ERROR!! el valor ingresado no es valido, vuleva a ingresar')],
				[sg.Button('OK')]]	
	if tipo=='datos':		
		window= sg.Window('ERROR!!', error_datos)
	if tipo=='nombre':
		window= sg.Window('ERROR!!', error_nombre)
	if tipo=='opcion':
		window= sg.Window('ERROR!!', error_opcion)
	event, values= window.read()
	if event=='OK':
		window.close()
		
def validar_datos(nombre,juego_jugado):
	aux=True
	if os.path.isfile('registrar_jugadores.json'):
		archivo=open('registrar_jugadores.json', 'r')
		datos= json.load(archivo)
		archivo.close()
		if juego_jugado in datos.keys():
			jugadores=datos[juego_jugado]
			if nombre in jugadores.keys():
				aux=False
	return aux
	
def leer_datos(juego_jugado):
	ingreso= [	[sg.Text('ingresar tu nombre, quedara registrada la partida!')],
				[sg.Text('ingrese su nombre: ',size=(15,1)), sg.Input(key='nombre',size=(20,1))],
				[sg.Button('Registrar',size=(15,1))]]
	window= sg.Window('Registrar datos!', ingreso)
	nombre=''
	while True:
		event, values=window.read()	
		if event ==None:								#en caso de que cierre la ventana de forma forzosa
			break
		if event=='Registrar':
			if values['nombre']=='': 	#reviso si los campos del input estan vacias o no
				error('datos')
			else:
				if validar_datos(values['nombre'],juego_jugado):
					nombre=(values['nombre'])
					break
				else:
					error('nombre')
	window.close()
	return nombre

def crear_archivo(juego_jugado,estructura):
	nuevo={juego_jugado:estructura}	
	with open('registrar_jugadores.json', 'w')as arc:
		json.dump(nuevo, arc, indent=4)
		arc.close()
		
def registrar_jugadores(juego_jugado, resultado):
	nombre=leer_datos(juego_jugado)	
	if nombre !='':						#pregunto si es vacia en caso de que se saliera de la ventana de forma 'forzosamente' y haci no guardo valores vacios
		jugador={nombre:{										#genero la estructura con los datos del jugador la cual
			'resultado':resultado,								#se va a guardar en el archivo
			'juego':juego_jugado}}	
		if os.path.isfile('registrar_jugadores.json'): 			#reviso si el archivo existe 					
			archivo= open('registrar_jugadores.json', 'r+')		
			dato = json.load(archivo)
			archivo.seek(0,0)
			if juego_jugado in dato.keys():					#el archivo esta dividido por los campos de cada juego	
				dato[juego_jugado].update(jugador)			#por cada juego se guarda los datos del jugador que lo jugo
			else:
				dato.setdefault(juego_jugado, jugador)
			json.dump(dato, archivo, indent=4)
			archivo.close()
		else:
			crear_archivo(juego_jugado,jugador) 				#genero el archivo y guardo los datos

def menu():
	menus = [
			[sg.Text('		||MENU||',)],
			[sg.Text('Elegi el juego que quieres jugar.')],
			[sg.Text('	1. Ahorcado',size=(30,1))],
			[sg.Text('	2. TA-TE-TI',size=(30,1))],
			[sg.Text('	3. Otello',size=(30,1))],
			[sg.Text('ingrese la opcion: ',size=(15,1)), sg.Input(key='opcion' ,size=(15,1))],
			[sg.Button('Jugar', size=(15,1)),sg.Button('Exit',size=(15,1))]
			] 
	
	window= sg.Window('juegos!!', menus)
	
	opc=''
	while True:
		event,values= window.read()
		if event == 'Jugar':
			opc=values['opcion']
			if (opc!='1') and (opc!='2') and (opc!='3'):		#verifico que se ingreso bien la opcion del juego a jugar
				error('opcion')
			else:
				break
		if (event == 'Exit') or (event == None):
			opc =event
			break
	window.close()
	return opc
	
def main(args):
	
	sigo_jugando = True
	while sigo_jugando:

		opcion = menu()									#modifique los main de de cada juego para que me retorne el
		if opcion == '1':								#resultado de la partida, solo le agregue variable 						
			resultado=hangman.main()
			registrar_jugadores('ahorcado',resultado)	#al finalizar la partida invoco un menu para que se registre el jugador
		elif opcion == '2':
			resultado=tictactoeModificado.main()
			registrar_jugadores('tateti',resultado)
		elif opcion == '3':
			resultado=reversegam.main()
			registrar_jugadores('Otello',resultado)
		elif opcion == 'Exit' or opcion == None:
			sigo_jugando = False
		
if __name__ == '__main__':
	
	import sys
	sys.exit(main(sys.argv))
