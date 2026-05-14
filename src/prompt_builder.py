import datetime
import os

from .config import MAX_FEWSHOT_EXAMPLES


def build_fewshot_examples(df_few_shot, max_examples=MAX_FEWSHOT_EXAMPLES):
    exemplos = []

    for _, row in df_few_shot.head(max_examples).iterrows():
        entrada = row.get('attacked', row.get('title'))
        saida   = row['normalized']

        exemplos.append(
            f'Entrada: "{entrada}"\nSaída: "{saida}"'
        )

    return "\n\n".join(exemplos)


def build_fewshot_prompt(items_batch, df_few_shot, max_examples=MAX_FEWSHOT_EXAMPLES):
    few_shot_str = build_fewshot_examples(df_few_shot, max_examples)

    itens_str = "\n".join([f'"{item}"' for i, item in enumerate(items_batch)])

    prompt = f"""
        Você é um sistema especializado em normalização de descrições de produtos de notas fiscais brasileiras.
        Seu objetivo é padronizar descrições sujas/abreviadas para um formato legível e consistente.

        Formato:
        NOME MARCA [EXTRAS]

        Regras gerais:
        - Tudo em MAIÚSCULO
        - NÃO inventar informações
        - NÃO excluir informações, apenas ordenar elas de forma correta
        - NÃO mudar a ordem das informações
        - NÃO incluir quantidade nem unidade (ex: 500ML, 2L, CX, UN, etc)
        - NÃO incluir códigos ou abreviações de embalagem (CX, PCT, FD, DZ, etc)

        Sobre EXTRAS:
        - Informações como cor, sabor, fragrância, essência, tipo, modelo, variante
        - Só incluir cor se o produto realmente tiver cor (ex: roupas, tintas, etc)
        - NÃO usar "S/C" para produtos sem cor
        - Se não houver cor -> NÃO colocar nada
        - Exemplos: PRETO, TRADICIONAL, BAUNILHA, NEUTRO, LIGHT, ZERO
        - Não repetir informação

        Exemplos:
        {few_shot_str}

        Itens:
        {itens_str}

        REGRAS DE SAÍDA (OBRIGATÓRIO):
        - Retorne exatamente {len(items_batch)} linhas
        - Uma linha por item
        - NÃO numere
        - NÃO explique
        - NÃO adicione texto extra
        - NÃO pule linhas
    """

    # # salvando o prompt construído
    # output_dir = "data/output"
    # os.makedirs(output_dir, exist_ok=True)

    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # file_path = os.path.join(output_dir, f"prompt_{timestamp}.txt")

    # with open(file_path, "w", encoding="utf-8") as f:
    #     f.write(f"TOTAL_ITENS: {len(items_batch)}\n\n")
    #     f.write(prompt)

    return prompt