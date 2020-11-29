from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.core.audio import SoundLoader
import math
import time

# Define o elemento "raquete"
class Raquete(Widget):
    """
    Define a raquete do nosso jogo. Também faz a verificação de colisão
    da raquete com a bolinha à fim de inverter sua direção.
    """

    # Cada raquete mantém seu placar
    placar = NumericProperty(0)
  
    # Carrega o som da colisão do disco com a raquete
    sound_disco_raquete = SoundLoader.load("audio/sfx-disco_raquete.mp3")

    # Declara as variaveis que iremos usar para identificar a "força" na hora da batida
    tx1 = 1
    ty1 = 1
    t1 = 1
    acc = 1

    # Define a colisão da raquete com a bola
    def rebate_bola(self, bola):

        # Calculo das distâncias entre os widgets para definir se houve colisão
        dx = self.center_x - bola.center_x
        dy = self.center_y - bola.center_y
        distancia = math.hypot(dx, dy)

        # Condição onde sera atribuida a pos anterior a colisão
        if (self.width + bola.width/2)*1.5 > distancia > (self.width + bola.width/2)/1.5:
            self.tx1 = self.center_x
            self.ty1 = self.center_y 
            self.t1 = time.time()

        # Verifica se houve a colisão do widget "raquete" com o widget "bola"
        if distancia <= (self.width + bola.width)/2:
            
            # Toca o áudio da colisão disco - raquete
            if self.sound_disco_raquete:
                self.sound_disco_raquete.play()

            # Atribuição da pos no momento da colisão
            tx2 = self.center_x
            ty2 = self.center_y 
            t2 = time.time()

            # Calculo das variações
            dt = t2 - self.t1
            tdx = tx2 - self.tx1
            tdy = ty2 - self.ty1
            td = math.hypot(tdx, tdy)

            # print("\nBateu\n", "Variação x: ", tdx, "Variação y: ", tdy, "Variação t: ", dt, "Variação dist", td) 

            # Define velocidade ganha pela bola
            if dt != 0:
                # Limita a aceleração para poder acompanhar o movimento da bola em 5 e valor minio em .2
                if (td/dt >= 2000):
                    self.acc = 5
                elif (td/dt >= 400):
                    self.acc = (td/dt)/400
                elif (td/dt >= 100):
                    self.acc = (td/dt)/400
                elif (dt > 0.35):
                    self.acc = 0
                else:
                    self.acc = 0.2
                
                # print("Aceleração: ", acc, "Velocidade", td/dt)
            
            # Seta velocidade da bola em 0 evitar bugs
            bola.velocidade = 0, 0

            # Pega tulpa da posição da bola na hora da colisão
            bx, by = bola.pos

            if distancia < (self.width + bola.width)/8:
                vetor_x = 0
                vetor_y = 0
            else:
            # Define um vetor resultante dados as posições e distancias no momento da colisão
                razao_x = (-dx)/(math.pi**2) + bx
                razao_y = (-dy)/(math.pi**2) + by
                vetor_x = (bx - razao_x)*self.acc
                vetor_y = (by - razao_y)*self.acc
                # print("Aceleração final: ", acc)

            # Seta a velcidade da bola resultante da colisão
            bola.velocidade = (-vetor_x) , (-vetor_y) 