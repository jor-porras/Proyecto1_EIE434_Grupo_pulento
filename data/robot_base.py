"""
Módulo robot_base.py - Tarea 1 Programación 2
Contiene las funciones para:
- Cargar los datos experimentales del paper (Tablas 6,7,8)
- Generar trayectorias ideales entre waypoints
- Simular lecturas del sensor LiDAR RPLIDAR S2
"""

import numpy as np  # Para operaciones matemáticas y arrays

# =============================================================================
# 1. FUNCIÓN: cargar_experimentos()
# =============================================================================
def cargar_experimentos():
    """
    Crea un diccionario de diccionarios con los resultados de las Tablas 6, 7 y 8.
    
    Estructura de salida:
    {
        "exp1": {"politica": "PPO", "ambiente": "real", "ruta": "simple", ...},
        "exp2": {"politica": "PPO-Mask", ...},
        ...
    }
    
    Total de 12 experimentos: 
    - Tabla 6: 2 experimentos (real, simple)
    - Tabla 7: 2 experimentos (real, compleja)
    - Tabla 8: 8 experimentos (simulación, con diferentes parámetros)
    """
    
    # Diccionario principal que contendrá todos los experimentos
    experimentos = {}
    
    # ----- TABLA 6: Ambiente real, ruta simple -----
    # (valores extraídos del paper; como no tengo los números exactos, pongo ejemplos)
    experimentos["exp1"] = {
        "politica": "PPO",
        "ambiente": "real",
        "ruta": "simple",
        "ISE": 434.99,
        "IAE": 135.93,
        "ITSE": 6932.79,
        "ITAE": 2601.61,
        "tiempo_s": None,
        "pasos": None,
        "reward_medio": None
    }
    
    experimentos["exp2"] = {
        "politica": "PPO-Mask",
        "ambiente": "real",
        "ruta": "simple",
        "ISE": 362.85,
        "IAE": 128.92,
        "ITSE": 5869.30,
        "ITAE": 2669.86,
        "tiempo_s": None,
        "pasos": None,
        "reward_medio": None
    }
    
    # ----- TABLA 7: Ambiente real, ruta compleja -----
    experimentos["exp3"] = {
        "politica": "PPO",
        "ambiente": "real",
        "ruta": "compleja",
        "ISE": 1120.45,      # valores de ejemplo, reemplazar con los reales del paper
        "IAE": 245.67,
        "ITSE": 15234.56,
        "ITAE": 3890.12,
        "tiempo_s": None,
        "pasos": None,
        "reward_medio": None
    }
    
    experimentos["exp4"] = {
        "politica": "PPO-Mask",
        "ambiente": "real",
        "ruta": "compleja",
        "ISE": 890.23,
        "IAE": 210.45,
        "ITSE": 12456.78,
        "ITAE": 3456.78,
        "tiempo_s": None,
        "pasos": None,
        "reward_medio": None
    }
    
    # ----- TABLA 8: Ambiente simulación (8 experimentos) -----
    # Normalmente varían: tiempo, pasos, reward_medio
    # Como el paper no está a la mano, pongo datos de ejemplo coherentes
    # Tú debes reemplazar con los valores reales de la Tabla 8 del paper
    
    # Para política PPO (4 experimentos)
    for i in range(1, 5):
        exp_key = f"exp{4 + i}"   # exp5, exp6, exp7, exp8
        experimentos[exp_key] = {
            "politica": "PPO",
            "ambiente": "simulacion",
            "ruta": f"sim_{i}",    # nombres: sim_1, sim_2, ...
            "ISE": 500 + i*50,
            "IAE": 150 + i*10,
            "ITSE": 8000 + i*500,
            "ITAE": 3000 + i*200,
            "tiempo_s": i * 5.0,
            "pasos": i * 50,
            "reward_medio": 0.8 - i*0.05
        }
    
    # Para política PPO-Mask (4 experimentos)
    for i in range(1, 5):
        exp_key = f"exp{8 + i}"   # exp9, exp10, exp11, exp12
        experimentos[exp_key] = {
            "politica": "PPO-Mask",
            "ambiente": "simulacion",
            "ruta": f"sim_{i}",
            "ISE": 450 + i*40,
            "IAE": 130 + i*8,
            "ITSE": 7200 + i*400,
            "ITAE": 2700 + i*150,
            "tiempo_s": i * 4.5,
            "pasos": i * 48,
            "reward_medio": 0.85 - i*0.04
        }
    
    return experimentos


# =============================================================================
# 2. FUNCIÓN: generar_trayectoria_ideal(waypoints, puntos_por_segmento=100)
# =============================================================================
def generar_trayectoria_ideal(waypoints, puntos_por_segmento=100):
    """
    Genera una trayectoria suave que pasa por todos los waypoints.
    
    Parámetros:
    - waypoints: lista de listas [[x0,y0], [x1,y1], ...]
    - puntos_por_segmento: cuántos puntos intermedios entre cada par de waypoints
    
    Retorna:
    - x_ideal: array de NumPy con las coordenadas X de la trayectoria
    - y_ideal: array de NumPy con las coordenadas Y de la trayectoria
    """
    
    # Listas vacías donde acumularemos todos los puntos
    x_ideal = []
    y_ideal = []
    
    # Recorremos los waypoints de a pares (actual y siguiente)
    for i in range(len(waypoints) - 1):
        # Punto actual y punto siguiente
        x1, y1 = waypoints[i]
        x2, y2 = waypoints[i + 1]
        
        # Generamos puntos intermedios con np.linspace
        # linspace(inicio, fin, cantidad) crea valores igualmente espaciados
        x_segmento = np.linspace(x1, x2, puntos_por_segmento)
        y_segmento = np.linspace(y1, y2, puntos_por_segmento)
        
        # Agregamos estos puntos a las listas principales
        # usamos extend en lugar de append para añadir todos los elementos de una vez
        x_ideal.extend(x_segmento)
        y_ideal.extend(y_segmento)
    
    # Convertimos las listas a arrays de NumPy (como pide el enunciado)
    return np.array(x_ideal), np.array(y_ideal)


# =============================================================================
# 3. FUNCIÓN: simular_lidar(n_sectores=36, d_min=0.5, d_max=30.0)
# =============================================================================
def simular_lidar(n_sectores=36, d_min=0.5, d_max=30.0):
    """
    Simula una lectura del sensor LiDAR RPLIDAR S2.
    
    Parámetros:
    - n_sectores: número de mediciones (ángulos) en 360 grados
    - d_min: distancia mínima del sensor (metros)
    - d_max: distancia máxima del sensor (metros)
    
    Retorna:
    - angulos_deg: array de ángulos en grados (0 a 360)
    - distancias: array de distancias simuladas (metros) con un obstáculo en los sectores 5 a 9
    - distancias_norm: array de distancias normalizadas entre 0 y 1
    """
    
    # 1. Crear los ángulos en grados (0°, 10°, 20°, ..., 350° si n_sectores=36)
    angulos_deg = np.linspace(0, 360, n_sectores, endpoint=False)  # endpoint=False para no repetir 360
    
    # 2. Generar distancias aleatorias uniformes entre d_min y d_max
    distancias = np.random.uniform(d_min, d_max, n_sectores)
    
    # 3. Simular un obstáculo: sectores 5 al 9 (índices) con distancias pequeñas (0.5 a 2.0 m)
    #    Nota: Python usa índices desde 0, así que el sector 5 es el índice 5 (el sexto sector)
    for i in range(5, 10):   # índices 5,6,7,8,9
        if i < n_sectores:   # por si n_sectores es menor a 10
            distancias[i] = np.random.uniform(0.5, 2.0)
    
    # 4. Normalizar las distancias: (d - d_min) / (d_max - d_min)
    #    Esto lleva todos los valores al rango [0,1]
    distancias_norm = (distancias - d_min) / (d_max - d_min)
    
    return angulos_deg, distancias, distancias_norm