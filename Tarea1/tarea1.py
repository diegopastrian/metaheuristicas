import time
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Costos (tomados del enunciado)
# ---------------------------------------------------------
costos = [60, 30, 60, 70, 130, 60, 70, 60, 80, 70, 50, 90, 30, 30, 100]

# ---------------------------------------------------------
# Conjuntos de cobertura (corregidos según la figura)
# ---------------------------------------------------------
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

# Lista de comunas (1 a 15)
comunas = list(range(1, 16))

# ---------------------------------------------------------
# Función para verificar la factibilidad (cubre todas las comunas?)
# ---------------------------------------------------------
def es_factible(solucion):
    """
    Verifica que cada comuna (1..15) esté cubierta por al menos un centro.
    Si alguna comuna j no está cubierta, retorna False.
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

# ---------------------------------------------------------
# Forward Checking
# ---------------------------------------------------------
def forward_check(solucion):
    """
    Verifica, para cada comuna j no cubierta todavía,
    si existe al menos una comuna no asignada que pueda cubrir j.
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

# ---------------------------------------------------------
# Función principal con Forward Checking
# ---------------------------------------------------------
def busqueda_forward_checking(index, solucion_actual, costo_actual, mejor_sol, mejor_costo, inicio, evolucion):
    """
    Aplica forward checking en cada nivel:
    - Si no se puede cubrir las comunas restantes con lo no asignado, se poda.
    """
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

    comuna = comunas[index]

    # Opción 1: no construir centro
    solucion_actual[comuna] = 0
    busqueda_forward_checking(index + 1, solucion_actual, costo_actual,
                              mejor_sol, mejor_costo, inicio, evolucion)

    # Opción 2: construir centro
    solucion_actual[comuna] = 1
    nuevo_costo = costo_actual + costos[comuna - 1]  # Ajuste en el índice
    busqueda_forward_checking(index + 1, solucion_actual, nuevo_costo,
                              mejor_sol, mejor_costo, inicio, evolucion)

    # Backtrack
    solucion_actual.pop(comuna)

# ---------------------------------------------------------
# Función para graficar la evolución de cada algoritmo
# ---------------------------------------------------------
def plot_evolution(evolution, label):
    """
    Dibuja la evolución del costo en función del tiempo
    para la técnica con nombre 'label'.
    """
    evolution.sort(key=lambda x: x[0])
    tiempos = [t for (t, _) in evolution]
    costos_vals = [cost for (_, cost) in evolution]
    plt.plot(tiempos, costos_vals, label=label)

# ---------------------------------------------------------
# Función principal
# ---------------------------------------------------------
def main():
    mejor_sol_forward = {}
    mejor_costo_forward = [float('inf')]
    evolucion_forward = []
    inicio3 = time.time()
    busqueda_forward_checking(0, {}, 0, mejor_sol_forward, mejor_costo_forward,
                              inicio3, evolucion_forward)
    tiempo_forward = time.time() - inicio3
    print(f"Solución con forward checking: Costo = {mejor_costo_forward[0]}, "
          f"Tiempo = {tiempo_forward:.4f} segundos")
    print("Centros construidos en comunas:",
          [i for i in mejor_sol_forward if mejor_sol_forward[i] == 1])
    print("Evolución (tiempo, costo):", evolucion_forward)
    
    # Graficar la evolución de todas las variantes
    plt.figure(figsize=(12, 8))
    plot_evolution(evolucion_forward, 'Forward Checking')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Costo Óptimo')
    plt.title('Evolución del Costo Óptimo vs Tiempo (Coberturas Corregidas)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
