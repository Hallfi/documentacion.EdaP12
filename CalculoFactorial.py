from multiprocessing import Process, Lock

# Función que calcula el factorial de un número
def factorial(n):
    """
    Calcula el factorial de un número n de forma iterativa.
    
    Parámetros:
    n (int): Número para el cual se calculará el factorial.
    
    Retorna:
    int: El factorial de n.
    """
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Función que calcula los factoriales en un rango específico y los guarda en un archivo
def guarda_factoriales(inicio, fin, lock):
    """
    Calcula los factoriales de un rango de números y guarda los resultados en un archivo.
    
    Parámetros:
    inicio (int): El inicio del rango de números.
    fin (int): El fin del rango de números.
    lock (Lock): Objeto Lock para sincronizar el acceso al archivo.
    """
    # Calculamos el factorial de cada número en el rango y almacenamos los resultados en una lista
    resultados = []
    for n in range(inicio, fin + 1):
        fact = factorial(n)
        resultados.append((n, fact))

    # Guardamos los resultados en el archivo de forma segura usando el lock
    with lock:
        with open("factorial.txt", "a") as f:
            for n, fact in resultados:
                f.write(f"Factorial de {n} es {fact}\n")

# Bloque principal para lanzar los procesos en paralelo
if _name_ == '_main_':
    # Número específico que queremos imprimir
    numero_especifico = 5  # Número para el cual queremos mostrar el factorial en pantalla

    # Definimos rangos para cada proceso, dividiendo el cálculo entre varios procesos
    rangos = [[1, 250], [251, 500], [501, 750], [751, 1000]]
    procs = []  # Lista para almacenar los procesos
    lock = Lock()  # Lock para sincronizar el acceso al archivo

    # Limpiamos el archivo de resultados al inicio para que no contenga datos de ejecuciones anteriores
    open("factorial.txt", "w").close()

    # Creamos y lanzamos los procesos
    for rango in rangos:
        # Creamos un proceso que ejecutará la función guarda_factoriales para su rango específico
        p = Process(target=guarda_factoriales, args=(rango[0], rango[1], lock))
        p.start()  # Iniciamos el proceso
        procs.append(p)  # Agregamos el proceso a la lista

    # Esperamos que todos los procesos terminen antes de continuar
    for p in procs:
        p.join()

    # Buscamos el factorial del número específico en el archivo
    factorial_especifico = None
    with open("factorial.txt", "r") as f:
        # Leemos línea por línea hasta encontrar el factorial del número específico
        for line in f:
            if f"Factorial de {numero_especifico} es" in line:
                factorial_especifico = line.strip()  # Guardamos la línea encontrada y salimos del bucle
                break

    # Imprimimos el factorial del número específico si fue encontrado
    if factorial_especifico:
        print(factorial_especifico)
    else:
        print(f"No se encontró el factorial de {numero_especifico} en el archivo.")

    # Mensaje final indicando que el cálculo ha terminado
    print("El cálculo ha finalizado. Los resultados se han guardado en 'factorial.txt'.")