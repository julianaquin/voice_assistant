import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# agregar opciones de voces de asistente
id1 = 'com.apple.speech.synthesis.voice.monica'
id2 = 'com.apple.speech.synthesis.voice.paulina'
id3 = 'com.apple.speech.synthesis.voice.diego'
id4 = 'com.apple.speech.synthesis.voice.jorge'
id5 = 'com.apple.speech.synthesis.voice.Victoria'


# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabación
        print('ya puedes hablar')

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-co")

            # prueba que pudo ingresar
            print("dijiste: " + pedido)

            # devolver pedido
            return pedido
        # en caso de que no comprenda el audioop
        except sr.UnknownValueError:

            # Prueba de que no comprendio el audio
            print('ups, no entendi')

            # devolver error
            return "sigo esperando"

        # en caso de no poder convertir el pedido a string
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print('ups, no hay servicio')

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendio el audio
            print('ups, algo ha salido mal')

            # devolver error
            return "sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id2)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crar una variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombre de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar que hora es
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora2 = f'En este momento son las {hora.hour} con {hora.minute} minutos y {hora.second} segundos '
    print(hora)
    hablar(hora2)


# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    print(hora)
    if hora.hour > 6 or hora.hour > 23:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos dias'
    else:
        momento = 'Buenas tardes'

    # saludar
    hablar(f'{momento} soy Julianito, su asistente personal. porfavor dime en que te puedo ayudar.')


# funcion cnetral del asistente
def pedir_cosas():

    # activar el saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:
        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        # respuestas a solicitudes que yo haga
        if 'abrir youtube' in pedido:
            hablar('con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('claro, estoy en eso')
            webbrowser.open('https://www.google.com/')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            print('pediste el dia')
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('entrando a internet')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Genial, ya pongo la reproducción')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'Encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('perdón, pero no la he encontrado')
                continue
        elif 'adios' or 'chao' in pedido:
            hablar('Descansa, cualquier cosa me avisas')
            break
