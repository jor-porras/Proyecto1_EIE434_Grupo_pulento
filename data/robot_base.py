"""
robot_base.py - Clase base para todos los robots de limpieza.
Encapsulamiento, cinemática, métodos estáticos y abstractos.
"""

import math

class RobotBase:
    def __init__(self, nombre, capacidad_carga, x_inicial=0.0, y_inicial=0.0, yaw_inicial=0.0):
        # Atributos privados (doble guion bajo)
        self.__nombre = nombre
        self.__capacidad_carga = capacidad_carga
        self.__bateria = 100.0
        self.__pos_x = x_inicial
        self.__pos_y = y_inicial
        self.__yaw = yaw_inicial
        self.__basura_recolectada = 0.0
        self.__step_dt = 0.1
        
        # Atributos públicos (la meta)
        self.target_x = 5.0
        self.target_y = 5.0

    # ---------- Getters (para acceder a los atributos privados) ----------
    def get_nombre(self):
        return self.__nombre

    def get_bateria(self):
        return self.__bateria

    def get_pos_x(self):
        return self.__pos_x

    def get_pos_y(self):
        return self.__pos_y

    def get_yaw(self):
        return self.__yaw

    def get_basura_recolectada(self):
        return self.__basura_recolectada

    # ---------- Métodos protegidos (para usar dentro de la clase y sus hijas) ----------
    def _actualizar_pose(self, x, y, yaw):
        """Sobrescribe la posición y orientación actuales."""
        self.__pos_x = x
        self.__pos_y = y
        self.__yaw = yaw

    def _reducir_bateria(self, cantidad):
        """Resta energía, sin dejar que baje de 0."""
        self.__bateria -= cantidad
        if self.__bateria < 0:
            self.__bateria = 0.0

    def _recolectar_basura(self, cantidad):
        """Añade basura respetando la capacidad máxima."""
        espacio = self.__capacidad_carga - self.__basura_recolectada
        if cantidad > espacio:
            cantidad = espacio
        self.__basura_recolectada += cantidad

    # ---------- Métodos estáticos (funciones de utilidad) ----------
    @staticmethod
    def calc_dist_to_goal(pos_x, pos_y, target_x, target_y):
        """Distancia euclidiana al objetivo."""
        dx = target_x - pos_x
        dy = target_y - pos_y
        return math.sqrt(dx*dx + dy*dy)

    @staticmethod
    def calc_yaw_error(pos_x, pos_y, yaw, target_x, target_y):
        """Error angular normalizado a [-pi, pi] entre la orientación actual y la dirección al objetivo."""
        angulo_meta = math.atan2(target_y - pos_y, target_x - pos_x)
        error = angulo_meta - yaw
        # Normalización
        error_norm = (error + math.pi) % (2 * math.pi) - math.pi
        return error_norm

    # ---------- Simulación cinemática (step) ----------
    def step(self, v, w):
        """
        Actualiza la pose del robot según velocidad lineal v y angular w.
        Retorna (reward, llegamos).
        """
        if self.__bateria <= 0:
            return 0.0, True

        dt = self.__step_dt

        # Nuevo yaw
        nuevo_yaw = self.__yaw + w * dt
        nuevo_yaw = (nuevo_yaw + math.pi) % (2 * math.pi) - math.pi

        # Nuevas posiciones
        nuevo_x = self.__pos_x + v * math.cos(nuevo_yaw) * dt
        nuevo_y = self.__pos_y + v * math.sin(nuevo_yaw) * dt

        # Guardar pose
        self._actualizar_pose(nuevo_x, nuevo_y, nuevo_yaw)

        # Calcular distancia y error angular
        distancia = self.calc_dist_to_goal(self.__pos_x, self.__pos_y, self.target_x, self.target_y)
        error_ang = self.calc_yaw_error(self.__pos_x, self.__pos_y, self.__yaw, self.target_x, self.target_y)

        # Recompensa
        reward = -distancia - abs(error_ang)

        llegamos = distancia < 0.5
        if llegamos:
            reward += 100.0

        return reward, llegamos

    # ---------- Métodos abstractos (las clases hijas deben implementarlos) ----------
    def mover(self):
        raise NotImplementedError("Las clases hijas deben implementar mover()")

    def limpiar(self):
        raise NotImplementedError("Las clases hijas deben implementar limpiar()")