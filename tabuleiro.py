from hashlib import new
import numpy as np
import math

#Classe de construção do tabuleiro
class Tabuleiro:
    #Construtora da classe
    #n representa o tamanho do tabuleiro e quantidade de rainhas
    #queens é o tabuleiro em forma de vetor, sendo o indíce a coluna e o valor a linha
    #binString é o tabuleiro em forma binária

    #OBS: É obrigatório que n seja passado
    def __init__(self, n, queens=[], binString=''):
        self.n = n

        #Caso o array do tabuleiro seja passado e o tabuleiro binário não, ele gera um valor apenas
        #para o tabuleiro binário
        if(not np.array_equal(queens, []) and binString == ''):
            self.queens = queens
            self.binString = self.representacaoBinaria(1, self.n)

        #Caso o array do tabuleiro binário seja passado, o tabuleiro de valores hexadecimais
        #é convertido a partir do binário
        elif (np.array_equal(queens, []) and binString != ''):
            self.binString = binString
            self.queens = self.gerarTabuleiroDeBin(self.binString)

        #Caso os dois arrays sejam passados, ele apenas atribui os valores com o self
        elif (not np.array_equal(queens, []) and binString != ''):
            self.queens = queens
            self.binString = binString

        #Caso nenhum valor seja passado, os dois tabuleiros são gerados 
        #aleatoriamente a partir de n
        else:
            self.queens = self.gerarTabuleiro()
            self.binString = self.representacaoBinaria(1, self.n)
            
    #Função para gerar um tabuleiro aleatório.            
    def gerarTabuleiro(self):
        queens = np.random.randint(1, self.n + 1, size=(self.n))
        return queens
    
    #Função para gerar o tabuleiro a partir da variável stringBin
    def gerarTabuleiroDeBin(self, queens):
        nBits = math.ceil(math.log(self.n, 2))
        tabuleiro = [(int(queens[i:i+nBits], 2) + 1) for i in range(0, len(queens), nBits)]
        return tabuleiro
    
    #Função para retornar uma representação binária do tabuleiro a partir do vetor queens
    def representacaoBinaria(self, minValue, maxValue):
        binString = ''
        nBits = math.ceil(math.log(self.n, 2))
        for e in self.queens:
            binString += bin(e - minValue)[2:].zfill(nBits)
        return binString
    
    #Função de avaliação do tabuleiro
    #a função começa calculando o total de pares possíveis de rainhas não atacantes
    
    #esse calculo é dado pela combinação do número de rainhas
    #dois a dois, a partir disso basta subtrair esse valor da quantidade de
    #ataques entre as rainhas que encontramos o número de pares de rainhas não
    #atacantes no tabuleiro.
    def avaliarTabuleiro(self):
        if hasattr(self, 'n_pares_nao_atacantes'):
            return self.n_pares_nao_atacantes
        
        n_pares_nao_atacantes = (self.n*(self.n-1))/2
        for i in range(0, self.n):
            for j in range(i + 1, self.n):
                if self.queens[i] == self.queens[j]:
                    n_pares_nao_atacantes -= 1
                elif self.queens[i] + (j - i) == self.queens[j]:
                    n_pares_nao_atacantes -= 1
                elif self.queens[i] - (j - i) == self.queens[j]:
                    n_pares_nao_atacantes -= 1
        self.n_pares_nao_atacantes = n_pares_nao_atacantes
        return n_pares_nao_atacantes
    
    #Função para printar o tabuleiro:
    def print_tabuleiro(self):
        matriz_rainha = np.zeros((self.n,self.n))
        for i in range(self.n):
            for j in range(self.n):
                matriz_rainha[i][j] = 0
        for i in range(self.n):            
            for j in range(self.n):
                if self.queens[j] == i+1:                
                    matriz_rainha[i][j] = 1 
        matriz_texto = "+"
        for i in range(self.n):
            matriz_texto += "---"
        matriz_texto += "+\n|"
        for i in range(self.n):
            matriz_texto += ""
            for j in range(self.n):
                if matriz_rainha[i][j] == 0:
                    matriz_texto += " . "
                else:
                    matriz_texto += " Q "
                if j == self.n-1:
                    if i == self.n-1:
                        matriz_texto += "|\n"
                    else:
                        matriz_texto += "|\n|"
        matriz_texto += "+"
        for i in range(self.n):
            matriz_texto += "---"
        matriz_texto += "+\n"
        matriz_texto += "|"
        for i in range(self.n):
            matriz_texto += "   "
        matriz_texto += "|\n"
        matriz_texto += "+"
        for i in range(self.n):
            matriz_texto += "---"
        matriz_texto += "+\n"
        print(matriz_texto)

