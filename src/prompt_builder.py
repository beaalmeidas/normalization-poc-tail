from .config import MAX_FEWSHOT_EXAMPLES


def build_fewshot_examples(df_few_shot, max_examples=MAX_FEWSHOT_EXAMPLES):
    exemplos = []

    for _, row in df_few_shot.head(max_examples).iterrows():
        entrada = row['item_nao_normalizado']
        saida   = row['item_normalizado']

        exemplos.append(
            f'Entrada: "{entrada}"\nSaída: "{saida}"'
        )

    return "\n\n".join(exemplos)


def build_fewshot_prompt(items_batch, df_few_shot, max_examples=MAX_FEWSHOT_EXAMPLES):
    few_shot_str = build_fewshot_examples(df_few_shot, max_examples)

    itens_str = "\n".join([f'{i+1}. "{item}"' for i, item in enumerate(items_batch)])

    prompt = f"""
        Você é um sistema especializado em normalização de descrições de produtos de notas fiscais brasileiras.
        Seu objetivo é padronizar descrições sujas/abreviadas para um formato legível e consistente.

        Formato:
        NOME MARCA [EXTRAS]

        Regras gerais:
        - Tudo em MAIÚSCULO
        - NÃO inventar informações
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

        Responda com uma linha por item, na mesma ordem.
        Sem explicações.
    """
    return prompt