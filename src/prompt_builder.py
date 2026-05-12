from .config import MAX_FEWSHOT_EXAMPLES


def build_fewshot_examples(df_few_shot, max_examples=MAX_FEWSHOT_EXAMPLES):
    exemplos = []

    for _, row in df_few_shot.head(max_examples).iterrows():
        entrada = row.get('attacked', row.get('title'))
        saida   = row['normalized']

        # Sem aspas nos exemplos para a LLM não repetir esse padrão na saída
        exemplos.append(
            f'Entrada: {entrada}\nSaída: {saida}'
        )

    return "\n\n".join(exemplos)


def build_fewshot_prompt(items_batch, df_few_shot, max_examples=MAX_FEWSHOT_EXAMPLES):
    few_shot_str = build_fewshot_examples(df_few_shot, max_examples)

    # Numerando os itens explicitamente para facilitar o parsing
    itens_str = "\n".join([f'{i+1}. {item}' for i, item in enumerate(items_batch)])
    n = len(items_batch)

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

        Itens para normalizar (total: {n}):
        {itens_str}

        INSTRUÇÕES DE RESPOSTA:
        - Responda EXATAMENTE {n} linhas, uma por item, na mesma ordem
        - Cada linha deve começar com o número do item seguido de ponto e espaço: "1. ", "2. ", etc.
        - SEM aspas, SEM explicações, SEM linhas extras
    """
    return prompt
