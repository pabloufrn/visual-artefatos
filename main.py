import requests
import json
import csv
import graph_gen 

def menu_principal():
	print(
		"----------------------------------\n" \
		"Gerador de visualição de artefatos\n" \
		"----------------------------------\n" \
		"1) Gerar grafo gerado por issues. \n" \
		"2) Gerar grafo gerado por pulls.  \n" \
		"r) Restaurar banco de dados.      \n" \
		"s) Sair da ferramenta.			   \n" \
		"----------------------------------")
	resposta = input("--> ")
	if(resposta == '1'):
		graph_gen.gerar_grafo_issues()
	elif(resposta == '2'):
		graph_gen.gerar_grafo_pulls()
	elif(resposta == 'r'):
		graph_gen.resetar_dados()
	elif(resposta == 's'):
		print('|!| Você saiu do programa.')
	else:
		print('|#| Resposta invalida.')
		return menu_principal()


if __name__ == '__main__':
	menu_principal()
    