from robot_base import RobotBase
import random


class RobotTresRuedas(RobotBase):

    def __init__(self, nombre, radio_rueda):

        super().__init__(nombre, 20.0)

        self.radio_rueda = radio_rueda
        self.ruedas_calibradas = False
    def calibrar_giro(self):
        print(f"Calibrando triciclo con radio de rueda {self.radio_rueda}")
        self.ruedas_calibradas = True

    def mover(self):
        recompensa, finalizado = self.step(v=0.8, w=0.2)
        return recompensa, finalizado
    
    def limpiar(self):
        self._gastar_bateria(2.0)
        basura = random.uniform(0.5, 1.5)
        self._recolectar_basura(basura)

class RobotOruga(RobotBase):

    def __init__(self, nombre, tension_oruga):

        super().__init__(nombre, 50.0)

        self.tension_oruga = tension_oruga
    def ajustar_tension(self):
        print(f"tension ajustada {self.tension_oruga}")
    
    def mover(self):
         recompensa, finalizado = self.step(v=0.3, w=0.8)
         return recompensa, finalizado
            
    def limpiar(self):
            self._gastar_bateria(4.5)
            basura = random.uniform(2.0, 4.0)
            self._recolectar_basura(basura)

class RobotDron(RobotBase):

    def __init__(self, nombre, altura_maxima):
        super().__init__(nombre, 5.0)
        self.altura_maxima = altura_maxima  
        self.en_vuelo = False

    def despegar(self):
        print(f"Solicitud de despegue generada. Altura máxima:{self.altura_maxima}")
        self.en_vuelo=True
    
    def mover(self):
        if self.en_vuelo==True:
          recompensa, finalizado = self.step(v=2.5, w=1.0)
          return recompensa, finalizado
        
        elif (self.en_vuelo) == False:
          return 0.0, False
    
    def limpiar(self):
        if self.en_vuelo==True:
            self._gastar_bateria(3.0)
            basura = random.uniform(0.1, 0.4)
            self._recolectar_basura(basura)
        elif self.en_vuelo==False:
            print("el dron no se encuentra en vuelo")
