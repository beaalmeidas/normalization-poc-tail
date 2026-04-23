from .pre_process import preprocess
from .prompt_builder import build_prompt, montar_prompt_batch
from .llm_client import call_llm
from .post_process import postprocess
def run_pipeline(data, client, model_id, df_few_shot, batch_size=10):
    results = []

    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]

        batch_pre = [preprocess(x)["raw"] for x in batch]

        prompt = montar_prompt_batch(batch_pre, df_few_shot)

        response = call_llm(client, model_id, prompt)

        linhas = response.split("\n")
        linhas = [l.strip() for l in linhas if l.strip()]

        for original, linha in zip(batch, linhas):
            final = postprocess(linha)

            results.append({
                "original": original,
                "normalized": final
            })

    return results