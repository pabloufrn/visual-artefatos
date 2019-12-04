# -*- encoding: utf-8

import requests
import json
import csv
import graph_gen
import terminal_interface
from action import terminal, graph
def menu_principal():
	print(
		"----------------------------------\n" \
		"Gerador de visualização de artefatos\n" \
		"----------------------------------\n" \
		"1) Gerar grafo gerado por issues. \n" \
		"2) Gerar grafo gerado por pulls.  \n" \
		"3) Gerar grafo gerado por commits.\n" \
		"4) Gerar gráfico de participação  \n" \
		"em issues.                        \n" \
		"5) Obter histórico de arquivo.    \n" \
		"6) Informações dos repositorio.   \n" \
		"r) Restaurar banco de dados.      \n" \
		"s) Sair da ferramenta.			   \n" \
		"----------------------------------")
	resposta = input("--> ")
	if(resposta == '1'):
		# graph_gen.gerar_grafo_issues()
		graph.issues()
	elif(resposta == '2'):
		# graph_gen.gerar_grafo_pulls()
		graph.pulls()
	elif(resposta == '3'):
		graph_gen.gerar_grafo_commits()
	elif(resposta == '4'):
		graph_gen.gerar_grafico_issues_part()
	elif(resposta == '5'):
		terminal_interface.ver_historico_arquivo()
	elif(resposta == '6'):
		terminal.show_repo_info()
	elif(resposta == 'r'):
		graph_gen.resetar_dados()
	elif(resposta == 's'):
		print('|!| Você saiu do programa.')
	else:
		print('|#| Resposta invalida.')
		return menu_principal()

if __name__ == '__main__':
	menu_principal()
