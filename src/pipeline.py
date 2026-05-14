import re
import time
import pandas as pd
from .config import BATCH_SIZE
from .pre_process import preprocess
from .prompt_builder import build_fewshot_prompt
from .llm_client import call_llm
from .post_process import postprocess
from .utils import ensure_dir


def parse_llm_response(response: str, expected: int):
    # Estratégia 1: linhas numeradas "1. item"
    numbered = re.findall(r'^\d+\.\s+(.+)', response, re.MULTILINE)
    if len(numbered) == expected:
        return numbered

    if len(numbered) > 0:
        print(f"    [WARN] Linhas numeradas: {len(numbered)}, esperado: {expected}")

    # Estratégia 2: fallback — linhas não-vazias sem cabeçalhos
    linhas = [
        l.strip()
        for l in response.split("\n")
        if l.strip() and not l.strip().lower().startswith(
            ("saída", "entrada", "item", "resposta", "normaliz")
        )
    ]
    linhas = [re.sub(r'^["\']|["\']$', '', l) for l in linhas]

    if len(linhas) == expected:
        return linhas

    print(f"    [WARN] Fallback falhou: {len(linhas)} linhas, esperado: {expected}")
    return None


def run_pipeline(
        data,
        client,
        model_id,
        df_few_shot,
        batch_size=BATCH_SIZE,
        output_path="data/output/normalized.csv",
    ):
    results = []
    total = len(data)
    batches_ok = 0
    batches_fail = 0

    ensure_dir("data/output")

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

        # Sleep curto — o retry no call_llm já lida com 503
        time.sleep(2)

        if not response:
            print(f"    [ERRO] LLM não retornou resposta para o batch {batch_num}\n")
            batches_fail += 1
            continue

        linhas = parse_llm_response(response, len(preprocessed_batch))

        if linhas is None:
            print(f"    [ERRO] Parsing falhou no batch {batch_num}")
            print(f"    Preview da resposta:\n{response[:400]}\n")
            batches_fail += 1
            continue

        for processed_item, linha in zip(preprocessed_batch, linhas):
            final = postprocess(linha, processed_item["medidas"])
            results.append({
                "original": processed_item["original"],
                "attacked": processed_item["attacked"],
                "normalized": final
            })

        # Salva incrementalmente após cada batch bem-sucedido
        pd.DataFrame(results).to_csv(output_path, index=False)
        batches_ok += 1
        print(f"    [OK] {len(linhas)} itens → CSV atualizado ({len(results)} total)\n")

    print(f"\n=== Pipeline finalizado: {batches_ok} batches OK, {batches_fail} falhas ===")
    print(f"=== Total de resultados: {len(results)} de {total} ===\n")
    return results
