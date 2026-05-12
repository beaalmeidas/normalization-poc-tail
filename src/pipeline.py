import re
import time
from .config import BATCH_SIZE
from .pre_process import preprocess
from .prompt_builder import build_fewshot_prompt
from .llm_client import call_llm
from .post_process import postprocess


def parse_llm_response(response: str, expected: int) -> list[str] | None:
    """
    Tenta extrair exatamente `expected` linhas da resposta da LLM.
    Estratégia 1: procura linhas numeradas "1. ", "2. ", etc.
    Estratégia 2: fallback para linhas não-vazias simples.
    Retorna None se não conseguir o número certo de linhas.
    """
    # Estratégia 1: extrai linhas numeradas explicitamente
    numbered = re.findall(r'^\d+\.\s+(.+)', response, re.MULTILINE)
    if len(numbered) == expected:
        return numbered

    if len(numbered) > 0:
        print(f"    [WARN] Linhas numeradas encontradas: {len(numbered)}, esperado: {expected}")

    # Estratégia 2: fallback — linhas não-vazias, sem cabeçalhos óbvios
    linhas = [
        l.strip()
        for l in response.split("\n")
        if l.strip() and not l.strip().lower().startswith(("saída", "entrada", "item", "resposta", "normaliz"))
    ]

    # Remove aspas caso a LLM tenha colocado
    linhas = [re.sub(r'^["\']|["\']$', '', l) for l in linhas]

    if len(linhas) == expected:
        return linhas

    print(f"    [WARN] Fallback também falhou: {len(linhas)} linhas, esperado: {expected}")
    return None


def run_pipeline(
        data,
        client,
        model_id,
        df_few_shot,
        batch_size=BATCH_SIZE
    ):
    results = []
    total = len(data)
    batches_ok = 0
    batches_fail = 0

    for i in range(0, total, batch_size):
        batch = data[i:i+batch_size]
        batch_num = i // batch_size + 1
        print(f"[Batch {batch_num}] Itens {i+1}–{i+len(batch)} de {total}")

        preprocessed_batch = [
            {
                **preprocess(item["attacked"]),
                "original": item["original"],
                "attacked": item["attacked"]
            }
            for item in batch
        ]

        prompt = build_fewshot_prompt(
            [item["raw"] for item in preprocessed_batch],
            df_few_shot
        )

        response = call_llm(client, model_id, prompt)

        time.sleep(15)

        if not response:
            print(f"    [ERRO] LLM não retornou resposta para o batch {batch_num}\n")
            batches_fail += 1
            continue

        linhas = parse_llm_response(response, len(preprocessed_batch))

        if linhas is None:
            print(f"    [ERRO] Não foi possível extrair {len(preprocessed_batch)} linhas do batch {batch_num}")
            print(f"    Resposta recebida:\n{response[:500]}\n")
            batches_fail += 1
            continue

        for processed_item, linha in zip(preprocessed_batch, linhas):
            final = postprocess(linha, processed_item["medidas"])
            results.append({
                "original": processed_item["original"],
                "attacked": processed_item["attacked"],
                "normalized": final
            })

        batches_ok += 1
        print(f"    [OK] {len(linhas)} itens processados\n")

    print(f"\n=== Pipeline finalizado: {batches_ok} batches OK, {batches_fail} falhas ===")
    print(f"=== Total de resultados gerados: {len(results)} de {total} ===\n")
    return results
