from .config import BATCH_SIZE
from .pre_process import preprocess
from .prompt_builder import build_prompt, build_fewshot_prompt
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
        batch = data[i:i+batch_size]

        batch_pre = [preprocess(x) for x in batch]

        prompt = build_fewshot_prompt(
            [item["raw"] for item in batch_pre],
            df_few_shot
        )

        response = call_llm(client, model_id, prompt)

        if not response:
            print("\n--- LLM falhou para esse batch\n")
            continue

        linhas = response.split("\n")
        linhas = [l.strip() for l in linhas if l.strip()]

        for original, linha in zip(batch, linhas):
            final = postprocess(linha)

            results.append({
                "original": original,
                "normalized": final
            })

    return results