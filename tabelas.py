import pdfplumber 
import pandas as pd

def remover_pontos(linhas):
    for linha in linhas:
        for i, item in enumerate(linha):
            if '.' in item:
                linha[i] = item.replace('.', '')
    return linhas

def posicao_primeiro_estado(linha):
    for i, item in enumerate(linha):
        if '(' in item:
            return i
    return -1

def posicao_segunda_cidade(linha):
    for i, item in enumerate(linha):
        if '-' in item:
            return i+1
    return -1

def posicao_segundo_estado(linha):
    for i, item in enumerate(linha):
        if '(' in item and i > posicao_primeiro_estado(linha):
            return i
    return -1

def ajustar_linhas(linhas):
    linhas_ajustadas = []
    for i, linha in enumerate(linhas):
        if len(linha)>10: #Linha com nome de uma das cidades composto
            estado = posicao_primeiro_estado(linha)
            if estado > 2: #Primeira cidade com nome composto - Tratar
                cidade = ''
                for i in range(1, estado):
                    cidade = cidade + ' ' + linha[i]
                linha[1] = cidade.strip()
                linha = [linha[0], linha[1]] + linha[estado:]
                linhas_ajustadas.append(linha)
            estado2 = posicao_segundo_estado(linha)
            print(estado2)
        else:
            linhas_ajustadas.append(linha)
    return linhas_ajustadas
        
with pdfplumber.open('planilha.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        texto = page.extract_text()
        if i == 0:
            linhas = texto.split('\n')
            linhas = linhas[7:]
        else:
            linhas += texto.split('\n')
    for i,linha in enumerate(linhas):
        if 'Fonte' in linha:
            linhas = linhas[:i-1]
            break
    linhas = [linha.split() for linha in linhas]
    for linha in linhas:
        if len(linha) == 5:
            linhas.remove(linha)
    linhas = remover_pontos(linhas)
    linhas = ajustar_linhas(linhas)
    for linha in linhas:
        print(len(linha), linha)
