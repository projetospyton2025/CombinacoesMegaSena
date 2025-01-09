from itertools import combinations
import requests

def validar_numeros(numeros):
    """Valida a lista de números fornecida"""
    if len(numeros) < 7:
        raise ValueError("Mínimo de 7 números necessários")
    if len(numeros) > 60:
        raise ValueError("Máximo de 60 números permitidos")
    if any(n < 1 or n > 60 for n in numeros):
        raise ValueError("Os números devem estar entre 1 e 60")
    if len(set(numeros)) != len(numeros):
        raise ValueError("Números não podem ser repetidos")
    return True

def gerar_combinacoes(numeros, tamanho):
    """Gera todas as combinações possíveis dos números fornecidos"""
    return list(combinations(sorted(numeros), tamanho))

def verificar_resultado(jogos):
    """Verifica os jogos contra o último resultado da Mega Sena"""
    try:
        response = requests.get("https://loteriascaixa-api.herokuapp.com/api/megasena/latest")
        if response.status_code != 200:
            raise Exception("Erro ao obter resultado da Mega Sena")
        
        dados = response.json()
        numeros_sorteados = [int(n) for n in dados['dezenas']]
        
        resultado = {
            'concurso': dados['concurso'],
            'data': dados['data'],
            'numeros': numeros_sorteados,
            'jogos': []
        }
        
        for jogo in jogos:
            acertos = len(set(jogo) & set(numeros_sorteados))
            resultado['jogos'].append({
                'combinacao': sorted(jogo),
                'acertos': acertos
            })
        
        return resultado
        
    except Exception as e:
        raise Exception(f"Erro ao verificar resultado: {str(e)}")