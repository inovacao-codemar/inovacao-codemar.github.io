# ======================================================================================================================
# SCRIPT DE SORTEIO AUTOMÁTICO DE GRUPOS INDIVIDUAIS
# Autor: Hygor Rasec
#
# Este código realiza o sorteio e organização de grupos com base na lista de inscritos que participaram individualmente.
#
# Lógica principal:
# - Prioriza a formação de grupos com 5 participantes.
# - Garante que os primeiros grupos sejam os mais completos.
# - Grupos menores (com 4 ou 3 integrantes) aparecem apenas ao final.
# - Sempre que possível, distribui participantes com funções diferentes e idades variadas nos primeiros grupos.
# - Gera um arquivo .txt com o resultado final de forma clara e legível.
# =======================================================================================================================


import random
from collections import defaultdict

# Participantes
participants = [
    {"name": "Brunno Teixeira Soares", "age": 19, "roles": ["Designer Gráfico"]},
    {"name": "Juan Victo Laurindo Teixeira da Silva", "age": 22, "roles": ["Designer Gráfico"]},
    {"name": "maicon vieira da silva", "age": 28, "roles": ["Engenheiro de Produto"]},
    {"name": "Fernanda Trindade cotta Xavier", "age": 13, "roles": ["Game Designer"]},
    {"name": "Victor Ângelo Bastos Ferreira", "age": 19, "roles": ["Game Designer"]},
    {"name": "Kauan Costa Coelho", "age": 16, "roles": ["Programador(a)", "Designer Gráfico", "Game Designer"]},
    {"name": "Pedro Vitor Salema Fernandes", "age": 24, "roles": ["Programador(a)"]},
    {"name": "Jonathan Coutinho de Moura Cruz", "age": 26, "roles": ["Programador(a)"]},
    {"name": "Pamela martinho", "age": 34, "roles": ["Roteirista / Narrativa"]},
    {"name": "Gustavo Alves Rios Pontes", "age": 11, "roles": ["Roteirista / Narrativa"]},
    {"name": "Adriele Silva Santos", "age": 23, "roles": ["Tester"]},
    {"name": "Enzo Longhi de Carvalho", "age": 19, "roles": ["Designer Gráfico"]},
    {"name": "Ryan Carvalho da silva", "age": 21, "roles": ["Tester"]},
    {"name": "Daniel Rocha Tavares da Silva", "age": 29, "roles": ["Programador(a)"]},
    {"name": "Maria Clara D'Ávila Santos", "age": 23, "roles": ["Programador(a)"]},
    {"name": "Douglas de Carvalho Galhardo", "age": 30, "roles": ["Programador(a)"]},
    {"name": "João Pedro Gomes Paulino", "age": 25, "roles": ["Programador(a)"]},
    {"name": "Murillo Reis Pereira", "age": 30, "roles": ["Tester"]},
    {"name": "Gabriel Cardoso de Lemos", "age": 21, "roles": ["Tester"]},
    {"name": "Henry Frazão Bispo", "age": 21, "roles": ["Designer Gráfico"]},
    {"name": "Michel kadesh daSilva santos", "age": 31, "roles": ["Programador(a)"]},
    {"name": "Lucas Ferreira Nobre", "age": 33, "roles": ["Programador(a)"]},
    {"name": "roberto lins brigida junior", "age": 22, "roles": ["Programador(a)"]},
    {"name": "Pedro Henrique de Moraes Penaforte Parreiras", "age": 36, "roles": ["Game Designer", "Designer Gráfico"]},
    {"name": "André Schuenck Benther", "age": 41, "roles": ["Game Designer"]},
    {"name": "Jefté Lopes Bastos", "age": 25, "roles": ["Indefinido"]},
    {"name": "Juliana Medeiros de Burity", "age": 21, "roles": ["Roteirista / Narrativa", "Áudio"]},
    {"name": "Igor Fernandes Barreto", "age": 29, "roles": ["Programador(a)"]},
    {"name": "Lucas Oliveira da Silva", "age": 23, "roles": ["Programador(a)", "Designer Gráfico", "Game Designer", "Roteirista / Narrativa", "Tester"]},
    {"name": "Sergio Stellet", "age": 35, "roles": ["Game Designer"]},
    {"name": "joão pietro soares santos", "age": 22, "roles": ["competidor"]},
    {"name": "Gabriel poubel Moura filho", "age": 20, "roles": ["Tester"]},
]

MIN_SIZE = 3
MAX_SIZE = 5
ESSENTIAL_ROLES = {"programador(a)", "designer gráfico", "game designer", "tester", "roteirista / narrativa"}


# Geração de tamanhos de grupos viáveis
def generate_group_sizes(total):
    sizes = []

    # Quantos grupos de 5 cabem?
    full_groups_of_5 = total // MAX_SIZE
    remainder = total % MAX_SIZE

    sizes = [5] * full_groups_of_5

    if remainder == 0:
        pass
    elif remainder == 1:
        # Ex: 31 -> [5, 5, 5, 5, 5, 5], sobra 1 (inválido), então ajusta dois grupos
        if len(sizes) >= 2:
            sizes[-1] = 4
            sizes[-2] = 4
            sizes.append(4)  # agora soma 32 (total de pessoas inscritas individualmente)
        else:
            raise Exception("Não foi possível formar grupos com os critérios.")
    elif remainder == 2:
        if len(sizes) >= 1:
            sizes[-1] = 4
            sizes.append(4)  # soma 32 (total de pessoas inscritas individualmente)
    elif remainder == 3:
        sizes.append(3)
    elif remainder == 4:
        sizes.append(4)

    return sizes

# Distribuição balanceada
def distribute_groups(participants):
    group_sizes = generate_group_sizes(len(participants))
    groups = [[] for _ in group_sizes]
    used_names = set()

    # Ordena por quantidade de funções
    participants.sort(key=lambda p: -len(p["roles"]))

    # Etapa 1: funções essenciais
    for role in ESSENTIAL_ROLES:
        eligible = [p for p in participants if role in map(str.lower, p["roles"]) and p["name"] not in used_names]
        random.shuffle(eligible)
        for i, p in enumerate(eligible):
            for j in range(len(groups)):
                group_roles = {r.lower() for m in groups[j] for r in m["roles"]}
                if p["name"] not in used_names and len(groups[j]) < group_sizes[j] and role not in group_roles:
                    groups[j].append(p)
                    used_names.add(p["name"])
                    break

    # Etapa 2: preencher com restante, evitando repetição de função
    remaining = [p for p in participants if p["name"] not in used_names]
    remaining.sort(key=lambda p: p["age"])

    group_fill_index = 0
    for p in remaining:
        while len(groups[group_fill_index]) >= group_sizes[group_fill_index]:
            group_fill_index += 1
        groups[group_fill_index].append(p)

    return groups

# Gerar os grupos
groups = distribute_groups(participants)

with open("grupos_sorteados.txt", "w", encoding="utf-8") as file:
    for i, group in enumerate(groups, 1):
        file.write(f"\n{'=' * 40}\n")
        file.write(f"Grupo {i} - {len(group)} integrantes\n")
        file.write(f"{'=' * 40}\n")
        for p in group:
            nome = p['name'].title()
            idade = p['age']
            funcoes = ", ".join(p['roles'])
            file.write(f"{nome} - {idade} anos - {funcoes}\n")
