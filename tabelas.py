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
    for i in range(len(linha)-1, 0, -1):
        if '(' in linha[i]:
            return i
    return -1

def remover_hifem(linhas):
    linhas_ajustadas = []
    for linha in linhas:
        for i, item in enumerate(linha):
            if '-' in item:
                linha.pop(i)
            #if ')' in item:
            #    linha[i] = item.replace(')', '')
            #    linha[i] = linha[i].replace('(', '')
        linhas_ajustadas.append(linha)
    return linhas_ajustadas

def remover_parenteses(linhas):
    linhas_ajustadas = []
    for linha in linhas:
        for i, item in enumerate(linha):
            if '(' in item:
                linha[i] = item.replace('(', '')
                linha[i] = linha[i].replace(')', '')
        linhas_ajustadas.append(linha)
    return linhas_ajustadas

def ajustar_linhas_primeira_cidade(linhas):
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
            else:
                linhas_ajustadas.append(linha)
        else:
            linhas_ajustadas.append(linha)
    return linhas_ajustadas

def ajustar_linhas_segunda_cidade(linhas):
    linhas_ajustadas = []
    for i, linha in enumerate(linhas):
        if len(linha)>9: #Linha com nome da segunda cidade composto
            estado = posicao_primeiro_estado(linha)
            estado2 = posicao_segundo_estado(linha)
            
            cidade = ''
            for i in range(estado+1, estado2):
                cidade = cidade + ' ' + linha[i]
            linha[3] = cidade.strip()
            linha = [linha[0], linha[1],linha[2],linha[3]] + linha[estado2:]
            linhas_ajustadas.append(linha)
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
    linhas = ajustar_linhas_primeira_cidade(linhas)
    linhas = remover_hifem(linhas)
    linhas = ajustar_linhas_segunda_cidade(linhas)
    linhas = remover_parenteses(linhas)
    print(len(linhas))
    for linha in linhas:
        print(len(linha), linha)
    df = pd.DataFrame(linhas, columns=['UF', 'Cidade1', 'Cidade2', 'Estado1', 'Estado2','Ida','Volta','Total','pass.km'])
    df.to_csv('tabela.csv', index=False, encoding='utf-8')