# Masked Cross-Attention Steering for Multi-Concept Erasure

This repository contains the code, evaluation notebooks, steering vectors, prompts and output artifacts for our Computer Vision (AI3603) final project, **Masked Cross-Attention Steering for Multi-Concept Erasure**.

## Project Summary

The project studies inference-time concept unlearning in Stable Diffusion 1.4, with broad parent concepts such as **vehicle**, **furniture** and **hand tool**. Starting from the original **CASteer** framework, we analyze why single-vector steering struggles on semantically broad concepts, evaluate several multi-vector alternatives and propose a masked steering method that localizes erasure to relevant spatial regions in cross-attention.

## Method Overview

We build on the work of the paper **CASteer: Cross-Attention Steering for Controllable Concept Erasure** and evaluate the following approaches:

1. **Baseline generation**
   - Stable Diffusion 1.4 without unlearning.

2. **Single-vector CASteer**
   - One parent-concept steering vector is subtracted globally.

3. **Average vector subtraction**
   - The parent vector is combined with one averaged subconcept vector.

4. **SVD-based vector subtraction**
   - The parent vector is combined with principal directions derived from the subconcept vectors.

5. **K-Means subset selection**
   - The parent vector is combined with a reduced set of representative original subconcept vectors.

6. **Masked cross-attention steering**
   - The parent vector is used globally, while subconcept vectors are applied through a relative spatial gate derived from cross-attention maps.

## Evaluation Method

Each method is evaluated using four prompt categories:

- **Direct**: prompts that explicitly mention the target concept.
- **Adversarial**: prompts that imply the concept without naming it directly.
- **Neighboring**: prompts semantically close to the target concept that should remain intact.
- **Unrelated**: prompts unrelated to the concept, used to measure general image utility.

We report two aggregate metrics:

- **Robustness**: average CLIP score over Direct and Adversarial prompts. Lower is better after erasure.
- **Utility**: average CLIP score over Neighboring and Unrelated prompts. Higher is better.

## Key Results

| Method | Robustness | Utility | Conclusion |
|---|---:|---:|---|
| Baseline SD1.4 | 0.3096 | 0.3101 | Reference point before unlearning |
| Single-vector CASteer | 0.2866 | 0.3072 | Some erasure, but poor generalization across subconcepts |
| Average vector subtraction | 0.2860 | 0.3068 | Little improvement over single-vector steering |
| SVD vectors subtraction | 0.2344 | 0.2714 | Degradation in Utility
| K-Means subset selection | 0.2777 | 0.3056 | Better semantic coverage with lower overhead |
| Masked cross-attention steering | 0.2701 | 0.3055 | Best overall balance in the project |

## Repository Structure

All notebooks are designed to run on Google Colab Free Tier (T4 GPU).
### `CASteer_CV/`

This folder contains the core code and data dependencies used by the notebooks.

- `vehicle_vecs/`, `furniture_vecs/`, `handtool_vecs/`
  - Precomputed parent and subconcept steering vectors (`.pickle` files).
  - These correspond to the concept and subconcept vectors discussed in the report.

- `vehicle_eval.json`, `furniture_eval.json`, `handtool_eval.json`
  - Evaluation prompt sets for the four prompt categories: Direct, Adversarial, Neighboring and Unrelated.

- `controller.py`
  - Core CASteer controller used for standard steering experiments.

- `controller_attn_mod.py`
  - Modified controller used for the masked attention experiments.
  - Adds cross-attention capture needed to build the relative spatial gate.

- `compute_steering_vectors.py`
  - Utility script for computing steering vectors from positive/negative prompt pairs.

- `generate_casteer.py`
  - Script for generating images with steering vectors applied during inference.

- `construct_prompts.py`, `construct_prompts_mod.py`
  - Prompt-construction utilities used during vector computation and failure-case experiments.

- `imagenet_classes.txt`
  - Supporting file used by prompt generation utilities.

### `Evaluation/`

This folder contains the experiment notebooks, generated images and result JSON files for each evaluated method.

- `Baseline Evaluation/`
- `Single Vector Subtraction/`
- `Average Vector Subtraction/`
- `SVD Vectors Subtraction/`
- `K Means Vectors Subtraction/`
- `Masked Attention Evaluation/`

Each method folder follows the same pattern:

- notebook(s) used to run the experiment
- generated image folders split by prompt category
- JSON files containing CLIP-based evaluation results

### `CASteer Failure Cases Experiments.ipynb`

This notebook was used to generate **Figure 1** in the report. It demonstrates failure cases of single-vector concept erasure on broad semantic categories.

### `CASteer_MCE_FullPipe.ipynb`

This notebook was used to generate the main concept vector and 10 subconcept vectors. The subconcepts were generated by prompting the Qwen2.5-0.5BInstruct LLM.

## Report-Repository Mapping Table

| Report item | Description | Corresponding files in this repo |
|---|---|---|
| **Figure 1** | Qualitative failure cases of single-vector concept erasure | `CASteer Failure Cases Experiments.ipynb` |
| **Table 1** | Baseline CLIP scores before unlearning | `Evaluation/Baseline Evaluation/` and the three baseline result JSON files |
| **Table 2** | Single-vector CASteer results | `Evaluation/Single Vector Subtraction/` and the three `*_single_vec.json` files |
| **Table 3** | Averaging-based multi-vector results | `Evaluation/Average Vector Subtraction/` and the three `*_avg_results.json` files |
| **Table 4** | SVD-based results shown in the report | `Evaluation/SVD Vectors Subtraction/vehicle_svd_results.json` and `CASteer_MCE_Veh_SVD_EvalPipe.ipynb` |
| **Table 5** | K-Means representative vector selection results | `Evaluation/K Means Vectors Subtraction/` and the three `*_kmeans_results.json` files |
| **Table 6** | Masked cross-attention steering results | `Evaluation/Masked Attention Evaluation/` and the three `*_attn2_results.json` files |

Additional note:

- The image subfolders inside each evaluation method directory contain the qualitative generations corresponding to that experiment.
- These subfolders are organized by prompt category: `direct`, `adversarial`, `neighboring` and `unrelated`.

## Acknowledgment

This project builds on the original **CASteer** codebase:

- Paper: *CASteer: Cross Attention Steering for Controllable Concept Erasure*
- Original repository: https://github.com/Atmyre/CASteer

The Python utilities and supporting files inside `CASteer_CV/` are essential for running the notebooks and reproducing the experiments in this repository. These were taken and modified from the above official GitHub repository of the paper.
