# TextNorm - Normalization PoC (TAIL-UFPB)

TextNorm is a system for normalizing noisy, inconsistent, and semi-structured product descriptions from brazilian invoices.

It was developed under the Natural Language Processing directorate at TAIL, as a research-oriented, proof-of-concept project focused on text normalization methods, combining rule-based processing, data augmentation, and large language models (LLMs).

<br />

This project was published in the following repositories:
- https://github.com/beaalmeidas/textnorm-poc-tail
- https://github.com/TailUFPB/invoice-data-normalizer/tree/poc_beatriz_adriano 

<br />

### Table of contents
- [TextNorm - Normalization PoC (TAIL-UFPB)](#textnorm---normalization-poc-tail-ufpb)
    - [Table of contents](#table-of-contents)
  - [1-) Objectives](#1--objectives)
  - [2-) Methods](#2--methods)
  - [3-) Sources](#3--sources)
    - [Papers](#papers)
    - [Datasets](#datasets)
  - [4-) How to Run](#4--how-to-run)
  - [5-) Project Structure](#5--project-structure)
  - [6-) Authorship](#6--authorship)


---
## 1-) Objectives

- Normalize noisy product titles and invoice descriptions
- Handle real-world variations such as typos, ordering changes, and missing structure
- Preserve semantic meaning while enforcing a consistent format
- Reduce reliance on the LLM for deterministic transformations
- Study Attack Augmentation and the best way to use it to expand the dataset without introducing problems to the normalization system (*semantic-aware augmentation for structured product text*)

<br />

---
## 2-) Methods
- Attack Augmentation
- Regex rulings in pre-processing and post-processing
- Few-Shot prompting

<br />

---
## 3-) Sources

### Papers
- **PolyNorm: Few-Shot LLM-Based Text Normalization for Text-to-Speech**  
Michel Wong, Ali Alshehri, Sophia Kao, Haotian He (Apple Research)  
(https://arxiv.org/abs/2511.03080)

<br />

### Datasets
- **Octaprice's Ecommerce Product Dataset**
(https://github.com/octaprice/ecommerce-product-dataset)

<br />

---
## 4-) How to Run
**1.** Clone the repo and open the project in an IDE
```
git clone https://github.com/beaalmeidas/textnorm-poc-tail.git
```
<br />

**2.** Open a terminal, create a virtual environment and install the requirements
```
python -m venv venv

venv/Scripts/activate
// for mac/linux: source venv/bin/activate

pip install -r requirements.txt
```
<br />

**3.** Create the .env file according to .env-example and add your Gemini API key + desired model of Gemini. For this project, ```gemini-3.1-flash-lite-preview``` is used as it is temporarily free for use.

<br />

**4.** Run the starting script
```
python -m scripts.run
```
<br />

All feedback will appear in the terminal, and the output dataset will be available in the data/output folder.

<br />

---
## 5-) Project Structure
```
textnorm-poc-tail/
    │
    ├── data/
    │    │
    │    ├── initial/
    │    │    ├── itens_nf_normalizacao.csv
    │    │    ├── octaprice_mercadolivre_1.json
    │    │    └── octaprice_mercadolivre_2.json
    │    │
    │    ├── input/
    │    │    ├── attack.csv
    │    │    ├── test_supervised.csv
    │    │    ├── test.csv
    │    │    └── train_supervised.csv
    │    │
    │    └── output/
    │         └── normalized.csv
    │
    ├── scripts/
    │    ├── attack_augmentation.py
    │    ├── generate_datasets.py
    │    └── run.py
    │
    ├── src/
    │    ├── config.py
    │    ├── llm_client.py
    │    ├── pipeline.py
    │    ├── post_process.py
    │    ├── pre_process.py
    │    ├── prompt_builder.py
    │    ├── test_llm.py
    │    └── utils.py
    │
    ├── .env-example
    ├── .gitignore
    ├── README.md
    └── requirements.txt

```

<br />

---

## 6-) Authorship
Beatriz Almeida, Adriano Dias