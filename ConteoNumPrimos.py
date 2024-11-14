from multiprocessing import Process, Lock, Value

# Función que verifica si un número es primo
def primo(n):
    """
    Verifica si un número es primo.

    Parámetros:
    n (int): Número a verificar.

    Retorna:
    bool: True si el número es primo, False en caso contrario.
    """
    if n < 2:
        return False
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True

# Función que cuenta los números primos en un rango específico y actualiza el contador global
def cuenta_primos(inicio, fin, lock, total_primos):
    """
    Cuenta los números primos en un rango específico y actualiza un contador global.

    Parámetros:
    inicio (int): Inicio del rango.
    fin (int): Fin del rango.
    lock (Lock): Objeto Lock para sincronizar el acceso al archivo y a la variable compartida.
    total_primos (Value): Variable compartida para almacenar el conteo total de números primos.
    """
    # Genera solo números impares dentro del rango para optimizar
    nums = [i for i in range(inicio, fin, 2)]
    contador = 0  # Contador local de números primos en el rango

    # Verifica cada número en el rango para ver si es primo
    for n in nums:
        if primo(n):
            contador += 1

    # Actualiza el total de primos de forma segura y escribe en el archivo
    with lock:
        total_primos.value += contador  # Suma el contador local al contador global
        with open("resultados.txt", "a") as f:
            f.write(f"Rango {inicio}-{fin} tiene {contador} primos\n")

# Bloque principal para lanzar los procesos en paralelo
if _name_ == '_main_':
    # Lista de rangos para dividir el trabajo entre procesos
    rangos = [[1, 2500], [2501, 5000], [5001, 7500], [7501, 10000]]
    procs = []  # Lista para almacenar los procesos
    lock = Lock()  # Lock para sincronizar el acceso al archivo y la variable compartida
    total_primos = Value('i', 0)  # Variable compartida para contar todos los números primos encontrados

    # Limpia el archivo de resultados antes de iniciar el cálculo
    open("resultados.txt", "w").close()

    # Crea y lanza un proceso para cada rango en la lista de rangos
    for rango in rangos:
        p = Process(target=cuenta_primos, args=(rango[0], rango[1], lock, total_primos))
        p.start()  # Inicia el proceso
        procs.append(p)  # Agrega el proceso a la lista

    # Espera que todos los procesos terminen
    for p in procs:
        p.join()

    # Imprime el total de números primos encontrados en el rango de 1 a 10000
    print(f"Total de primos encontrados en el rango de 1 a 10000: {total_primos.value}")
    print("El cálculo ha finalizado. Los resultados se han guardado en 'resultados.txt'.")