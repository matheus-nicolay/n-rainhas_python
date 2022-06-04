import pandas as pd
import numpy as np
import plotly.express as px
from tabuleiro import Tabuleiro
from populacao import Populacao

def algoritmoGenetico(n_it, tamanho_pop, tamanho_tab, p_cross, p_mut, elitismo=False):
    popCorrente = Populacao(tamanho_pop, tamanho_tab, p_cross, p_mut, elitismo)
    for i in range(0, n_it):
        popCorrente = Populacao(tamanho_pop, tamanho_tab, p_cross, p_mut, elitismo, popCorrente.popIntermediaria)

        for tab in popCorrente.tabuleiros:
            Nttabuleiro = Tabuleiro(tamanho_tab, tab)
        
    return popCorrente


def testarAlgoritmoGenetico():
    iteracoes = 100
    populacao = 20
    tamanho_tab = 4
    prop_crossover = 0.5
    prop_mutacao = 0.1
    elitismo = True

    dfAlgoritmoGenetico = pd.DataFrame()

    resultado = algoritmoGenetico(iteracoes, populacao, tamanho_tab, prop_crossover, prop_mutacao, elitismo)
    

    dfAlgoritmoGenetico = dfAlgoritmoGenetico.append({
        "tamanho_tab": tamanho_tab,
        "populacao":  populacao,
        "iteracoes": iteracoes,
        "probabilidade_crossing": prop_crossover,
        "probabilidade_mutacao": prop_mutacao,
        "elitismo": elitismo,
        "media": calcularMediaEDesvioPadroaDaPopulacao(resultado, tamanho_tab)[0],
    }, ignore_index=True)

    
    for tabuleiro in resultado.tabuleiros:
        Nttabuleiro = Tabuleiro(tamanho_tab, tabuleiro)
        Nttabuleiro.print_tabuleiro()

    return dfAlgoritmoGenetico

def calcularMediaEDesvioPadroaDaPopulacao(populacao, tamanho_tab):
    a = []
    for tab in populacao.tabuleiros:
        a.append( Tabuleiro(tamanho_tab, queens=tab).avaliarTabuleiro() )
    
    return (np.mean(a), np.std(a))


dfAlgoritmoGenetico = testarAlgoritmoGenetico()
