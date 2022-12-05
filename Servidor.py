import socket

direccionip = socket.gethostbyname(socket.gethostname())
print("Tu direccion ip actual es: " , direccionip)
# creamos una entrada para el teclado la ip del servidor
host = input("En que direccion se va a alojar el servidor: ")
# creamos una entrada para el puerto del servidor
port = int(input("En que puerto va a funcionar: "))

# creamos el socket
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)
# vinculamos el host(ip) y el puerto con el servidor
sc.bind((host , port))
# ponemos el socket en escucha
sc.listen(1)

print("Servidor corriendo en el puerto ", port)


while True:
    # aceptamos todas las conexiones posibles, ademas esta nos devuelve la conexion y la direccion
    con , addr = sc.accept()
    # definimos el tamaño de los bloques
    respuesta = con.recv(2048).decode('utf-8')

    # creamos una lista para los requerimientos que se le de los separa por un espacio
    lista = respuesta.split(' ')
    # definimos que la primera posicion sea el metodo
    metodo = lista[0]
    # definimos que la segunda posicion sea la ruta
    ruta = lista[1]
    # imprimimos la duta
    print("Ruta solicitada: ",ruta)

    # creamos otras lista donde separemos con el caracter ?
    # ya que todo lo que se ponga despues de ese caracter 
    # no importara o no tendra relevancia alguna
    archivo = ruta.split('?')[0]
    archivo = archivo.lstrip('/')

    # si la ruta en la cual estamos entrando esta vacia significa 
    # que estamos ingresando a la raiz del servidor
    if(archivo == ''):
        # abrimos el archivo index del servidor
        archivo = 'index.html'
    
    # ejecutamos un bloque de prueba de errores por si no llegara a existir
    # un archivo nos pueda llegar a mandar un error
    try:
        # abrimos el archivo en formato rb que es lectura de bytes
        file = open(archivo , 'rb')
        respuesta = file.read()
        file.close()

        # creamos unos metodos para crear la cabezera
        header = 'HTTP/1.1 200 OK\n'

        # vemos cual es la extencion del archivo al cual queremos acceder
        if(archivo.endswith('.jpg')):
            mimetype = 'image/jpg'
        elif(archivo.endswith('.css')):
            mimetype = 'text/css'
        elif(archivo.endswith('.pdf')):
            mimetype = 'application/pdf'
        else:
            mimetype = 'text/html'
        # concatenamos el header con el mimetype del contenido que queremos
        # mostrar en la direccion del servidor
        header += 'Content-Type: '+str(mimetype)+'\n\n'

    except Exception as e:
        # mandamos a la cabecera que el archino no fue encontrado
        header = 'HTTP/1.1 404 Error Archivo no encontrado\n\n\n'
        respuesta = '<html><body>Error 404: Archivo no encontrado</body></html>'.encode('utf-8')
    
    # Mostramos al final el metodo get
    respuesta_final = header.encode('utf-8')
    # concatenemos la respuesta con la respuesta final
    respuesta_final += respuesta
    # mandamos la conexion
    con.send(respuesta_final)
    # cerramos la conexion
    con.close()

# Documentacion
# https://docs.python.org/3/howto/sockets.html
# https://developer.mozilla.org/es/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types