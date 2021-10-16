##########################imports###########################

import numpy as np
import matplotlib.pyplot as plt

########################## Variaveis globais ###########################

dimensao = 1000
iterations = 10
size = 10
filename = "newton"
colors = {0: "red", 1: "blue", 2: "green"}

############################### Classes ################################

class bloco:

    '''um bloco é um elemento de ponto, armazena suas coordenadas e a raiz
    a qual ele converge

    Attributes
    ----------
    self.x: float
    coordenada do ponto em x

    self.y: float
    coordenada do ponto em y

    self.root: int
    1, 2, 3, ... para as n raizes da funcao
    '''

    def __init__(self, x, y, root):
        self.x = x
        self.y = y
        self.root = root

    
class function:

    '''A funcao a ser usada deve ser definida na classe para acesso
    generico

    Attributes
    ----------
    self.raizes: dict
    dict de int -> complexo com numeracao da raiz e seu valor

    Methods
    -------
    value(x)
        returns valor da funcao em x
    
    derivative(x)
        returns valor da derivada em x

    wich_root(x)
        returns o numero da raiz mais proxima de x
        
    '''

    raizes = {0 : 1j, 1 : -1j, 2 : -1}

    def value(self, x):
        '''Avalia o valor da funcão em um ponto x
        
        Parameters
        ----------
        x : complex
            ponto a ser avaliado
        '''
        return pow(x,3) + pow(x, 2) + x + 1
    
    def derivative(self, x):
        '''Avalia o valor da derivada da funcão em um ponto x
        
        Parameters
        ----------
        x : complex
            ponto a ser avaliado
        '''
        return 1 + 2 * x + 3 * pow(x, 2)

    def wich_root(self, x):
        '''Avalia a raiz mais proxima de x
        
        Parameters
        ----------
        x : complex
            ponto a ser avaliado
        '''
        pivo = 10000000000
        for root in self.raizes:
            dist = ((self.raizes[root].imag - x.imag)**2 +
                    (self.raizes[root].real - x.real)**2)**0.5
            if dist < pivo:
                pivo = dist
                raiz = root
        return raiz

class malha:

    '''Define o objeto malha que representa o plano complexo no nosso problema

    Attributes
    ----------
    self.dimensao: int
        tamanho da matrix a ser definida

    self.size: int
        tamanho da area do plano a ser capturada
    
    self.x0: int
        x do canto inferior esquerdo da area capturada
    
    self.y0: int
        y do canto inferior esquerdo da area capturada
    
    self.block_size: float
        tamanho de cada bloco no plano
    
    self.matrix: matrix
        matriz que armazena os blocos
    
    self.func: function
        função a ser usada

    Methods
    -------
    iterate()
        realiza uma iteração do processo de newton nos pontos pelo process
    
    process(i, j)
        processa o ponto dado

    paint()
        define a raiz associada com cada ponto
        
    '''

    def __init__(self, dimensao, size):
        
        self.dimensao = dimensao
        self.size = size
        self.x0 = 0 - size/2
        self.y0 = 0 - size/2
        self.block_size = size / dimensao

        self.matrix = [[bloco(self.x0 + i * self.block_size, self.y0 + j * self.block_size, 0)
         for j in range(0,dimensao)]
         for i in range(0,dimensao)]

        self.func = function()

    def iterate(self):
        '''Realiza uma iteração sobre a matriz

        '''
        for i in range(0, self.dimensao):
            for j in range(0, self.dimensao):
                self.process(i, j)

    def process(self, i, j):
        '''Processa um ponto de coord i, j pelo processo de newton
        
        Parameters
        ----------
        i : float
            coord i

        j : float
            coord j
        '''
        point = complex(self.matrix[i][j].x, self.matrix[i][j].y)
        next = point - self.func.value(x=point)/self.func.derivative(x=point)
        self.matrix[i][j].x = next.real
        self.matrix[i][j].y = next.imag

    def paint(self):
        '''Define par acada ponto a raiz associada
    
        '''
        for i in range(0, self.dimensao):
            for j in range(0, self.dimensao):
                self.matrix[i][j].root = (
                    self.func.wich_root(
                        complex(self.matrix[i][j].x, self.matrix[i][j].y)
                        )
                    )


######################## Funcao Auxiliar Escrita #######################

def write(malha):

    '''Escreve em um arquivo de txt as raizes de cada ponto da malha
        
    Parameters
    ----------
    malha: malha
        malha a ser transcrita
    '''

    ext = 'out.dat'
    with open(filename + ext, 'w') as outfile:
        for line in malha.matrix:
            for elem in line:
                print(elem.root, end=' ', file=outfile)
            print(file=outfile)
        print(file=outfile)
    return filename+ext

def plot(file):
    '''Plota o arquivo txt gerado
        
    Parameters
    ----------
    file: String
        nome do arquivo
    '''
    imagem = (np.loadtxt(file) + 1)**0.001
    plt.imshow(imagem, cmap='inferno')
    plt.show()

############################## Main Program ############################

if __name__ == '__main__':

    minha_malha = malha(dimensao, size)

    for x in range(0, iterations):
        minha_malha.iterate()

    minha_malha.paint()
    file_name = write(minha_malha)
    plot(file_name)
