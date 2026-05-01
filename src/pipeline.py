import time
from .config import BATCH_SIZE
from .pre_process import preprocess
from .prompt_builder import build_fewshot_prompt
from .llm_client import call_llm
from .post_process import postprocess


def run_pipeline(
        data, 
        client, 
        model_id, 
        df_few_shot, 
        batch_size=BATCH_SIZE
    ):
    results = []

    for i in range(0, len(data), batch_size):
        # quebrando os dados de acordo com o tamanho de conjunto definido
        batch = data[i:i+batch_size]

        # rodando pré-processamento em cada item do conjunto de dados enviado
            # e retornando dicionário de infos
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

        # print("----- DEBUG -----")
        # print("Batch size:", len(preprocessed_batch))
        # print("Itens no batch:", [item["raw"] for item in preprocessed_batch])
        # print("Prompt length (chars):", len(prompt))
        # print("Prompt preview:\n", prompt[:300])
        # print("-----------------")

        response = call_llm(client, model_id, prompt)

        time.sleep(6)

        if not response:
            print("\n--- LLM falhou para esse batch\n")
            continue

        # quebrando a resposta da LLM em linhas
        linhas = response.split("\n")
        # removendo espaços antes/depois e linhas vazias
        linhas = [l.strip() for l in linhas if l.strip()]

        if len(linhas) != len(preprocessed_batch):
            print("\n--- Quantidade de linhas diverge entre os dados de input e a saída da LLM\n")
            continue

        for processed_item, linha in zip(preprocessed_batch, linhas):
            final = postprocess(
                linha,
                processed_item["medidas"]
            )

            results.append({
                "original": processed_item["original"],
                "attacked": processed_item["attacked"],
                "normalized": final
            })

    return results