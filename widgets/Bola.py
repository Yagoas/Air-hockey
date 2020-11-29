from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


# Define o elemento "bola"
class Bola(Widget):
    """
    Define a bola do jogo e mantém sua velocidade, a qual é um Vector
    contendo suas componentes de velocidade X e Y.
    """

    # Velocidade da bola
    velocidade_x = NumericProperty(0)
    velocidade_y = NumericProperty(0)

    # Velocidade
    velocidade = ReferenceListProperty(velocidade_x, velocidade_y)

    # Define a função de movimento da nossa bolinha
    def movimenta(self):
        # Função para movimentar a bola
        self.pos = Vector(*self.velocidade) + self.pos

    def movimenta_atrito(self):
        # Função movimentar a bola e desacelerar com o tempo
        self.velocidade = Vector(0.985 * self.velocidade_x, 0.985 * self.velocidade_y)
        self.pos = Vector(*self.velocidade) + self.pos
