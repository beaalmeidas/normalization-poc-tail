def load_prompt_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(template: str, examples: list, input_text: str) -> str:
    examples_str = ""

    for ex in examples:
        examples_str += f"Entrada: {ex['input']}\nSaída: {ex['output']}\n\n"

    return template.format(
        examples=examples_str,
        input=input_text
    )

def montar_few_shot_str(df_few_shot):
    exemplos = []

    for _, row in df_few_shot.iterrows():
        entrada = row['item_nao_normalizado']
        saida   = row['item_normalizado']

        exemplos.append(
            f'Entrada: "{entrada}"\nSaída: "{saida}"'
        )

    return "\n\n".join(exemplos)

def montar_prompt_batch(itens_batch, df_few_shot):
    few_shot_str = montar_few_shot_str(df_few_shot)

    itens_str = "\n".join([f'{i+1}. "{item}"' for i, item in enumerate(itens_batch)])

    prompt = f"""
Você é um sistema especializado em normalização de descrições de produtos de notas fiscais brasileiras.
Seu objetivo é padronizar descrições sujas/abreviadas para um formato legível e consistente.

Formato obrigatório:
NOME MARCA COR {...} - QUANTIDADE UNIDADE

Regras:
- MAIÚSCULO
- Se não houver cor = usar S/C
- NÃO inventar informação
- NÃO mudar a ordem

Exemplos:
{few_shot_str}

Itens:
{itens_str}

Responda com uma linha por item, na mesma ordem.
"""
    return prompt