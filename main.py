import csv
import os
from datetime import datetime
from pathlib import Path

arquivo_csv = 'estoque.csv'
campos = ['id', 'nome', 'quantidade', 'unidades', 'localização', 'valor', 'data_entrada', 'data_atualização', 'descrição']
data_agora = datetime.now()
nota_atualizacao = Path('nota_atualização.txt')

def inicializar_arquivo():
  
  arquivo_existe = os.path.exists(arquivo_csv)
    
  if not arquivo_existe:
    try:
      with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        print(f"Arquivo '{arquivo_csv}' criado com sucesso e cabeçalho adicionado.\n")
    except Exception as e:
        print(f"Erro ao criar arquivo: {e}")
  else:
        print(f"O arquivo '{arquivo_csv}' já existe. Inicialização ignorada.\n")
        
def carregar_dados():
  
  dados = []

  with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as arquivo:
    leitor = csv.DictReader(arquivo)
    for linha in leitor:
      linha['id'] = int(linha['id'])
      linha['quantidade'] = int(linha['quantidade'])
      linha['valor'] = float(linha['valor'])
      dados.append(linha)

  return dados

def salvar_dados(dados):
  
  with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as arquivo:
      escritor = csv.DictWriter(arquivo, fieldnames=campos)
      escritor.writeheader()
      escritor.writerows(dados)
  
  return dados

def validar_int(pergunta):
  while True:
    try:
      valor = int(input(pergunta))
    except ValueError:
      print("Entrada inválida, digite apenas números inteiros")
  
    if valor >= 0:
      return valor
    else:
      print("Entrada inválida, insira um valor positivo")

def unidade_medida():
  while True:
      escolha = validar_int("Defina uma unidade de medida:\n1 - Unidades\n2 - Caixas\n3 - Metros\n4 - Litros\n5 - Kg\n")

      match escolha:
        case 1:
          unid_medida = 'Unidades'
          return unid_medida
        case 2:
          unid_medida = 'Caixas'
          return unid_medida
        case 3:
          unid_medida = 'Metros'
          return unid_medida
        case 4:
          unid_medida = 'Litros'
          return unid_medida
        case 5:
          unid_medida = 'Kg'
          return unid_medida
        case _:
          print("Opção inválida.")
          continue

def localizacao():
  hc = validar_int("Defina onde está localizado:\n\nHC/Zona: ")
  rua = validar_int("Em qual corredor/rua está localizado: ")
  bloco = validar_int("Em qual bloco: ")
  nivel = validar_int("Em qual nível: ")
  localizacao = f"HC{hc}R{rua}B{bloco}N{nivel}"
  return localizacao

def arrumar_data(data):
  data_convertida = datetime.strftime(data, "%d/%m/%Y %H:%M:%S")
  return data_convertida

def escrever_nota(escolha, data, nome):
  if escolha == 'cadastro':
    nova_linha = f"{data} - {nome} foi cadastrado\n"
  elif escolha == 'atualização':
    nova_linha = f"{data} - {nome} foi atualizado\n"
  elif escolha == 'deletar':
    nova_linha = f"{data} - {nome} foi deletado\n"
  
  try:
    with nota_atualizacao.open(mode='a', encoding='utf-8') as n:
      n.write(nova_linha)
      print(f"Nova nota de atualização foi anotada em {nota_atualizacao}")
  except Exception as e:
      print(f"Ocorreu um erro ao escrever no arquivo: {e}")

def gerar_novo_id():
  
  dados = carregar_dados()

  if not dados:
    return 1

  ids_ocupados = []
  for m in dados:
    ids_ocupados.append(m['id'])
  
  novo_id = 1
  while True:
    if novo_id not in ids_ocupados:
      return novo_id
    novo_id += 1

def cadastrar():
  
  print("\n", "-" * 50, "\n")
  
  while True:
  
    novo_id =  int(gerar_novo_id())
    nome = input('Digite o nome: ')
  
    quantidade = validar_int('Digite a quantidade no estoque: ')
    
    unid_medida = unidade_medida()
 
    local = localizacao()

    try:
      valor = float(input("Digite o valor do produto: "))
    except ValueError:
      print("Entrada inválida, digite um número.")

    data_entrada = arrumar_data(data_agora)
    data_atualizacao = arrumar_data(data_agora)

    descricao = input("Digite a descrição do produto:\n")

    escrever_nota('cadastro', data_atualizacao, nome)

    with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as arquivo:
      escritor = csv.DictWriter(arquivo, fieldnames = campos)
      escritor.writerow({'id': novo_id, 'nome': nome, 'quantidade': quantidade, 'unidades': unid_medida, 'localização': local, 'valor': valor, 'data_entrada': data_entrada, 'data_atualização': data_atualizacao, 'descrição': descricao})

    continuar = input('\nDeseja cadastrar outro material? (s/n): ')
    if continuar.lower() != 's':
      print("\n", "-" * 50, "\n")
      break
    continue
  
def ler():

  print("-" * 150)
  dados = carregar_dados()
    
  if not dados:
    print('Nenhum material cadastrado')
  else:
    print(f"{'ID':<5} | {'Nome':<20} | {'Quantidade':<5} | {'Unidades':<10} | {'Localização':<15} | {'Valor':<6} | {'Entrada':<30} | {'Atualização':<30}")
    print("-" * 150)
    for m in dados:
      print(f"{m['id']:<5} | {m['nome']:<20} | {m['quantidade']:<10} | {m['unidades']:<10} | {m['localização']:<15} | {m['valor']:<6} | {m['data_entrada']:<30} | {m['data_atualização']:<30}")
  print("-" * 150, "\n")

def atualizar():

  ler()
  
  id_busca = validar_int('\nDigite o id do material que deseja alterar: \n')

  dados = carregar_dados()
  material_encontrado = False

  for m in dados:
    if int(m['id']) == id_busca:
      print(f"\nEditando: {m['nome']}\n")
      print("Caso não queira mudar aperte Enter\n")
      at_nome = input(f"Novo nome de {m['nome']}: \n") or m['nome'] 
      m['nome'] = at_nome
      
      at_quantidade = input(f'Deseja atualizar a quantidade (atual: {m['quantidade']})? (s/n): ')
      if at_quantidade.lower() == 's':
        m['quantidade'] = validar_int(f"Nova quantidade: \n")
      else:
         m['quantidade'] 
      
      at_unidades = input(f'Deseja atualizar a unidade de medida (atual: {m['unidades']})? (s/n): ')
      if at_unidades.lower() == 's':
        m['unidades'] = unidade_medida()
      else:
        m['unidades']
      
      at_localizacao = input(f'Deseja atualizar a localização (atual: {m['localização']})? (s/n): ')
      if at_localizacao.lower() == 's':
        m['localização'] = localizacao()
      else:
        m['localização']

      m['data_atualização'] = arrumar_data(data_agora)

      material_encontrado = True
      escrever_nota('atualização', m['data_atualização'], m['nome'])
      print("\n", "-" * 50, "\n")
      break
    
  
  if material_encontrado:
     salvar_dados(dados)
  else:
     print("Material não encontrado.\n")
     print("\n", "-" * 50, "\n")

def deletar():
  print("\n", "-" * 50, "\n")
  ler()
 
  id_busca = validar_int('\nDigite o id do material que deseja alterar: \n')
  
  dados = carregar_dados()
  
  novo_estoque = [m for m in dados if int(m['id']) != id_busca]

  for m in dados:
    if id_busca == int(m['id']):
      data_atualizacao = arrumar_data(data_agora)
      escrever_nota('deletar', data_atualizacao, m['nome'])

  if len(dados) > len(novo_estoque):
    salvar_dados(novo_estoque)
    print("Material deletado.")
    print("\n", "-" * 50, "\n")
  else:
    print("ID não encontrado\n")
    print("\n", "-" * 50, "\n")

def main():
  while True:
    print("1 - Cadastrar material")
    print("2 - Mostrar estoque")
    print("3 - Atualizar material")
    print("4 - Deletar material")
    print("5 - Finalizar")
    escolha = input("\nO que deseja fazer?\n")

    if escolha == '1':
      cadastrar()
    elif escolha == '2':
      ler()
    elif escolha == '3':
      atualizar()
    elif escolha == '4':
      deletar()
    elif escolha == '5':
      break
    else:
      print('\nOpção inválida.\n')
      continue

if __name__ == '__main__':
  inicializar_arquivo() 
  main()