import time
import matplotlib.pyplot as plt

nodos_visitados_forward = 0

costos = [60, 30, 60, 70, 130, 60, 70, 60, 80, 70, 50, 90, 30, 30, 100]
 #        1   2   3    4   5   6    7   8   9  10  11  12  13  14   15
cobertura = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], 
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0], 
    [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1], 
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0], 
    [0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1], 
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1], 
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1]  
]

comunas = list(range(1, 16))

def calcular_heuristica():
    """
    Calcula la heurística para la selección de la siguiente comuna
    - Se selecciona primero la comuna con menos vecinos.
    - Si hay empate, se selecciona la comuna con el menor costo.
    """
    # Calculamos el número de vecinos de cada comuna
    cobertura_count = {comuna: sum(cobertura[comuna-1]) for comuna in comunas}
    
    # Ordenamos las comunas primero por la cantidad de vecinos (de menos a más), luego por costo (menor costo primero)
    orden_heuristico = sorted(comunas, key=lambda comuna: (-cobertura_count[comuna], costos[comuna-1]))
    
    return orden_heuristico

def es_factible(solucion):
    """
    Verifica que se satisface la demanda de cada comuna
    """
    for j in comunas:
        cubierta = False
        for i in comunas:
            # Verifica si j está en la cobertura de algún i con x_i=1
            if cobertura[i-1][j-1] == 1 and solucion.get(i, 0) == 1:  # Cobertura binaria
                cubierta = True
                break
        if not cubierta:
            return False
    return True

def forward_check(solucion):
    """
    Observa si cada comuna j podrá ser cubierta a futuro por comuna i
    """
    unassigned = [i for i in comunas if i not in solucion]
    for j in comunas:
        # ¿j está cubierta por la asignación actual?
        cubierta_actual = any(
            cobertura[i-1][j-1] == 1 and solucion.get(i, 0) == 1
            for i in solucion
        )
        if not cubierta_actual:
            # j no está cubierta: debe haber al menos un 'i' en unassigned que pueda cubrirla
            if not any(cobertura[i-1][j-1] == 1 for i in unassigned):
                return False
    return True

def busqueda_forward_checking(index, solucion_actual, costo_actual, mejor_sol, mejor_costo, inicio, evolucion, orden):
    """
    Aplica forward checking en cada nivel:
    - Si no se puede cubrir las comunas restantes con lo no asignado, se poda.
    """
    global nodos_visitados_forward

    if costo_actual >= mejor_costo[0]:
        return

    # Comprobamos forward checking
    if not forward_check(solucion_actual):
        return

    if index == len(comunas):
        if es_factible(solucion_actual) and costo_actual < mejor_costo[0]:
            mejor_costo[0] = costo_actual
            mejor_sol.clear()
            mejor_sol.update(solucion_actual)
            evolucion.append((time.time() - inicio, costo_actual))
        return

    comuna = orden[index]

    # no construir centro
    solucion_actual[comuna] = 0
    nodos_visitados_forward += 1
    busqueda_forward_checking(index + 1, solucion_actual, costo_actual,
                              mejor_sol, mejor_costo, inicio, evolucion, orden)

    # construir centro
    solucion_actual[comuna] = 1
    nuevo_costo = costo_actual + costos[comuna - 1]  # Ajuste en el índice
    nodos_visitados_forward += 1
    busqueda_forward_checking(index + 1, solucion_actual, nuevo_costo,
                              mejor_sol, mejor_costo, inicio, evolucion, orden)

    # Backtrack
    solucion_actual.pop(comuna)

def main():
    global nodos_visitados_forward
    #hola lucowsky
    # 1. Ejecución sin heurística
    nodos_visitados_forward = 0
    mejor_sol_forward = {}
    mejor_costo_forward = [float('inf')]
    evolucion_forward_sin_heuristica = []
    inicio3 = time.time()
    busqueda_forward_checking(0, {}, 0, mejor_sol_forward, mejor_costo_forward,
                              inicio3, evolucion_forward_sin_heuristica, comunas)  # Ejecuta con el orden natural
    tiempo_forward_sin_heuristica = time.time() - inicio3
    print("\n===============================")
    print("Ejecución sin Heurística")
    print("===============================")
    print(f" - Costo Óptimo: {mejor_costo_forward[0]}")
    print(f" - Tiempo: {round(tiempo_forward_sin_heuristica * 1000, 2)} milisegundos")
    print(f" - Centros construidos en comunas: {', '.join(map(str, [i for i in mejor_sol_forward if mejor_sol_forward[i] == 1]))}")
    print(f" - Nodos visitados: {nodos_visitados_forward}")
    print("===============================\n")

    
    # 2. Ejecución con heurística
    nodos_visitados_forward = 0
    orden_heuristico = calcular_heuristica()
    print("\n===============================")
    print("Ejecución con Heurística")
    print("===============================")
    print(f" - Orden Heurístico: {', '.join(map(str, orden_heuristico))}")
    print(f" El orden heuristico: {orden_heuristico}")
    mejor_sol_forward = {}
    mejor_costo_forward = [float('inf')]
    evolucion_forward_con_heuristica = []
    inicio3 = time.time()
    busqueda_forward_checking(0, {}, 0, mejor_sol_forward, mejor_costo_forward,
                              inicio3, evolucion_forward_con_heuristica, orden_heuristico)  # Ejecuta con la heurística
    tiempo_forward_con_heuristica = time.time() - inicio3
    print(f" - Costo Óptimo: {mejor_costo_forward[0]}")
    print(f" - Tiempo: {round(tiempo_forward_con_heuristica * 1000, 2)} milisegundos")
    print(f" - Centros construidos en comunas: {', '.join(map(str, [i for i in mejor_sol_forward if mejor_sol_forward[i] == 1]))}")
    print(f" - Nodos visitados: {nodos_visitados_forward}")
    print("===============================")

    # Graficar costo vs tiempo
    plt.figure(figsize=(10, 6))
    
    # Extraer valores de evolución para cada método
    tiempos_sin_heuristica = [t for (t, _) in evolucion_forward_sin_heuristica]
    costos_sin_heuristica = [c for (_, c) in evolucion_forward_sin_heuristica]

    tiempos_con_heuristica = [t for (t, _) in evolucion_forward_con_heuristica]
    costos_con_heuristica = [c for (_, c) in evolucion_forward_con_heuristica]

    # Graficar ambas curvas
    plt.plot(tiempos_sin_heuristica, costos_sin_heuristica, label="Sin Heurística", marker='o')
    plt.plot(tiempos_con_heuristica, costos_con_heuristica, label="Con Heurística", marker='s')

    # Etiquetas
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Costo Total")
    plt.title("Evolución del Costo vs Tiempo para Forward Checking")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()