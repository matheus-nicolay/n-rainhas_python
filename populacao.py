import numpy as np
from tabuleiro import Tabuleiro

class Populacao:
    #Função de inicialização da população, que além de definir os tabuleiros que a compõem, também
    #calcula a população intermediária após serem aplicados os operadores
    def __init__(self, n, size, pc, pm, elitismo=False, tabuleiros = []):
        self.n = n
        self.size = size
        self.pc = pc
        self.pm = pm
        self.elitismo = elitismo
        self.tabuleiros = tabuleiros if not np.array_equal(tabuleiros, []) else self.gerarPopulacao()
        self.probabilidades = self.construirRoletaViciada()
        self.popIntermediaria = self.construirPopulacaoIntermediaria()
        self.popIntermediaria = self.realizarCrossover()
        self.popIntermediaria = self.realizarMutacao()
        
    #Função para gerar uma população aleátoria, chamada no caso de não forem passados tabuleiros
    #como parâmetro para a classe.
    def gerarPopulacao(self):
        tabuleiros = []
        for i in range(0, self.n):
            tabuleiros.append(list(Tabuleiro(self.size).queens))
        return tabuleiros
    
    #Função para construir uma roleta viciada, que se baseia em um vetor com cada um dos intervalos de probabilidade
    #possíveis, de maneira que todos os valores desse vetor somam 1.
    #Como esse função itera por todos os tabuleiros da população, já aproveitamos para também encontrar o 
    #individuo de melhor adaptação da população
    def construirRoletaViciada(self):
        probabilidades = []
        totalSum = 0
        self.melhorTabuleiro = self.tabuleiros[0]

        for i in self.tabuleiros:
            totalSum += Tabuleiro(self.size, queens=i).avaliarTabuleiro()
            probabilidades.append(totalSum)
            if(self.elitismo):
                self.melhorTabuleiro = i if Tabuleiro(self.size, queens=i).avaliarTabuleiro() > Tabuleiro(self.size, queens=self.melhorTabuleiro).avaliarTabuleiro() else self.melhorTabuleiro
        
        probabilidades = list(map(lambda x: x/totalSum, probabilidades))
        self.probabilidades = probabilidades
        return probabilidades
    
    #Função para construção da população intermediária, a cada iteração é gerado um número aleátorio
    #e a função se baseia em determinar em qual dos intervalos do vetor de probabilidades está esse número 
    #aleatório, como cada um desses intervalos está associado a um tabuleiro da população, esse tabuleiro, é então
    #adicionado a população intermediaria
    #Se o elitismo da população está habilitado o melhor indíviduo é transmitido diretamente para a população
    #intermediária.
    def construirPopulacaoIntermediaria(self):
        tabuleiros = []
        for i in range(0, self.n):
            randomNumber = np.random.random()
            for i in range(0, len(self.probabilidades)):
                if(self.probabilidades[i] > randomNumber):
                    tabuleiros.append(self.tabuleiros[i])
                    break
                    
        if(self.elitismo):
            tabuleiros[0] = self.melhorTabuleiro
        
        return tabuleiros
    
    #Função para atualizar a população intermediária após o cross over ser realizado
    #Se o elitismo da população está habilitado o melhor indíviduo é transmitido diretamente para a população
    #intermediária
    def realizarCrossover(self):
        tabuleiros = []
        for i in range(0, self.n, 2):
            randomNumber = np.random.random()
            if(randomNumber < self.pc):
                randomIndex = np.random.randint(1, self.size)
                novoTabuleiro1 = self.popIntermediaria[i][:(randomIndex)] + self.popIntermediaria[i + 1][(randomIndex):]
                novoTabuleiro2 = self.popIntermediaria[i + 1][:(randomIndex)] + self.popIntermediaria[i][(randomIndex):]
                tabuleiros.append(novoTabuleiro1)
                tabuleiros.append(novoTabuleiro2)
            else:
                tabuleiros.append(self.popIntermediaria[i])
                tabuleiros.append(self.popIntermediaria[i + 1])
                
        if(self.elitismo):
            tabuleiros[0] = self.melhorTabuleiro
        
        return tabuleiros
    
    #Função para atualizar a população intermediária após a mutação para cada um dos elementos
    #Se o elitismo da população está habilitado o melhor indíviduo é transmitido diretamente para a população
    #intermediária
    def realizarMutacao(self):
        tabuleiros = []
        for i in self.popIntermediaria:
            randomNumber = np.random.random()
            novoTabuleiro = i
            if(randomNumber < self.pm):
                randomIndex = np.random.randint(0, self.size)
                novoTabuleiro[randomIndex] = np.random.randint(1, self.size + 1)
            tabuleiros.append(novoTabuleiro)
        
        if(self.elitismo):
            tabuleiros[0] = self.melhorTabuleiro
        
        return tabuleiros