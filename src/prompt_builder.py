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