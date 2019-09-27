# -*- encoding: utf-8

import requests
import json
import csv
import graph_gen
import requests_cache 

def menu_principal():
	print(
		"----------------------------------\n" \
		"Gerador de visualição de artefatos\n" \
		"----------------------------------\n" \
		"1) Gerar grafo gerado por issues. \n" \
		"2) Gerar grafo gerado por pulls.  \n" \
		"3) Gerar grafo gerado por commits.\n" \
		"4) Gerar gráfico de participação  \n" \
		"em issues.                        \n" \
		"r) Restaurar banco de dados.      \n" \
		"s) Sair da ferramenta.			   \n" \
		"----------------------------------")
	resposta = input("--> ")
	if(resposta == '1'):
		graph_gen.gerar_grafo_issues()
	elif(resposta == '2'):
		graph_gen.gerar_grafo_pulls()
	elif(resposta == '3'):
		graph_gen.gerar_grafo_commits()
	elif(resposta == '4'):
		graph_gen.gerar_grafico_issues_part()
	elif(resposta == 'r'):
		graph_gen.resetar_dados()
	elif(resposta == 's'):
		print('|!| Você saiu do programa.')
	else:
		print('|#| Resposta invalida.')
		return menu_principal()


if __name__ == '__main__':
	requests_cache.install_cache('main_cache', expire_after=None)
	menu_principal()
    
