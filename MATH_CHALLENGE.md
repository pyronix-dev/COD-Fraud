# Competition Math Hallucination Detection Challenge

## Problem Description

Large language models are increasingly used for mathematical reasoning, but they frequently hallucinate solutions, misapply theorems, or make calculation errors. This challenge tests whether your model can detect subtle hallucinations in competition-level mathematics.

### The Challenge

You are given **800 statements** based on **200 verified competition math problems** from:
- **AIMO** (Australian Intermediate Mathematics Olympiad)
- **AMC 10/12** (American Mathematics Competitions)
- **AIME** (American Invitational Mathematics Examination)
- **PUMaC** (Princeton University Math Competition)
- **HMMT** (Harvard-MIT Mathematics Tournament)

Each statement is either:
- **TRUE (25%)**: Original problem with correct solution and reasoning
- **HALLUCINATION (75%)**: Contains exactly one critical error

Your task: Build a binary classifier predicting `is_hallucination` (1 = hallucination, 0 = true).

### Why This Is Hard

This dataset targets known LLM weaknesses in mathematical reasoning:

| Error Type | Description | Example |
|------------|-------------|---------|
| **Constant Shift** | Numbers changed by ±1 or ±2 | "7^2019 mod 100 has tens digit **5**" (correct: 4) |
| **Logic Error** | Sign/operator flip in reasoning | "This is F_{n-**2**}" (correct: F_{n+2}) |
| **Wrong Solution** | Correct problem, incorrect answer | "Area = **96**" (correct: 84) |

### Difficulty Tiers

| Tier | Source | Description |
|------|--------|-------------|
| Tier 1 | AMC 10 Basic | Arithmetic, basic algebra |
| Tier 2 | AMC 10/12 | Intermediate algebra, geometry |
| Tier 3 | AMC 12/AIME | Advanced topics, multi-step |
| Tier 4 | AIME/PUMaC/HMMT | Olympiad-level, creative insights |

### Chain of Thought

Each sample includes an average-length CoT (3-5 steps, 100-300 characters) showing the reasoning process. Hallucinations may have corrupted CoT with logical errors.

---

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `statement_id` | int | Row index (0 to 799) |
| `statement` | string | The math problem statement |
| `domain` | string | Subject area (Algebra, Geometry, Number Theory, Combinatorics, Probability) |
| `is_hallucination` | int | **Target**: 1 = hallucination, 0 = true |
| `error_type` | string | Type of error (Constant, Logic, Solution) - null for true |
| `the_truth` | string | The original correct problem statement |
| `correct_solution` | string | The verified correct answer |
| `source_id` | string | Problem ID (e.g., "AIMO001", "AMC003") |
| `source` | string | Competition name and year |
| `tier` | int | Difficulty level (1-4) |
| `cot` | string | Chain of Thought reasoning (3-5 steps) |

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Samples** | 800 |
| **Base Problems** | 200 |
| **TRUE** | 200 (25%) |
| **HALLUCINATION** | 600 (75%) |
| **Domains** | 5 (Algebra, Geometry, Number Theory, Combinatorics, Probability) |
| **Avg CoT Length** | ~150 characters |

### Error Type Distribution

| Error Type | Count |
|------------|-------|
| Constant | 200 |
| Logic | 200 |
| Solution | 200 |

### Tier Distribution

| Tier | Samples |
|------|---------|
| Tier 1 | ~80 |
| Tier 2 | ~200 |
| Tier 3 | ~240 |
| Tier 4 | ~280 |

---

## Evaluation

### Metric

Submissions evaluated using **F1 Score** for hallucination detection:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)

Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
```

- **TP** = Correctly identified hallucinations
- **FP** = True statements flagged as hallucinations
- **FN** = Hallucinations missed

### Why F1 Score?

- **High precision**: Don't flag correct math as wrong (maintain trust)
- **High recall**: Catch actual hallucinations (prevent misinformation)

---

## Submission Format

Submit a CSV file:

```csv
statement_id,is_hallucination
0,1
1,0
2,1
...
799,0
```

### Requirements

1. **Format**: CSV with UTF-8 encoding
2. **Header**: `statement_id,is_hallucination`
3. **statement_id**: 0 to 799 in order
4. **is_hallucination**: Binary (0 or 1) only
5. **Complete**: All 800 statements must have predictions

---

## Example Data Samples

### TRUE Statement
```
statement_id: 5
statement: "Find all integers x such that x² ≡ 1 (mod 8)."
domain: Mathematics - Number Theory
is_hallucination: 0
error_type: null
correct_solution: "x ≡ 1, 3, 5, 7 (mod 8)"
source: AIMO 2018
tier: 2
cot: "Check each residue: 0²=0, 1²=1, 2²=4, 3²=9≡1, 4²=16≡0, 5²=25≡1, 6²=36≡4, 7²=49≡1 (mod 8). So x² ≡ 1 when x ≡ 1, 3, 5, 7 (mod 8)."
```

### HALLUCINATION (Logic Error)
```
statement_id: 0
statement: "Find the number of binary strings of length 10 with no two consecutive 1s."
domain: Mathematics - Combinatorics
is_hallucination: 1
error_type: Logic
correct_solution: "144"
source: HMMT 2019
tier: 4
cot: "This is F_{n-2} = F₁₂ = 144, where F is the Fibonacci sequence."
```
*Error: Should be F_{n+2}, not F_{n-2}*

### HALLUCINATION (Wrong Solution)
```
statement_id: 3
statement: "In how many ways can 5 people sit around a circular table if two specific people must sit together?"
domain: Mathematics - Combinatorics
is_hallucination: 1
error_type: Solution
correct_solution: "48"
source: AIMO 2020
tier: 4
cot: "Treat the two specific people as one unit. Now we have 4 units to arrange in a circle: (4-1)! = 6 ways..."
```

---

## Baseline Approaches

### Rule-Based
- Verify numerical answers with symbolic computation (SymPy, Wolfram)
- Check Fibonacci/recurrence relations against known formulas
- Validate modular arithmetic step-by-step

### NLP Models
- Fine-tune BERT/RoBERTa on statement + CoT concatenation
- Use MathBERT or SciBERT for domain-specific embeddings
- Leverage NLI models for statement-solution consistency

### LLM-Based
- Prompt LLMs to verify with step-by-step checking
- Use self-consistency across multiple samples
- Tool-augmented verification (calculator, SymPy)

---

## Getting Started

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

# Load data
df = pd.read_csv('competition_math_hallucination.csv')

# Split
train, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df['is_hallucination'])

# Simple baseline: predict all as hallucination (baseline F1 ≈ 0.86)
y_pred = [1] * len(test)
f1 = f1_score(test['is_hallucination'], y_pred)
print(f"Baseline F1: {f1:.4f}")

# Your model here
# y_pred = model.predict(test[features])
# f1 = f1_score(test['is_hallucination'], y_pred)
```

---

## Research Applications

1. **Mathematical Reasoning Verification** - Detect LLM errors in proofs
2. **Educational Tools** - Automated checking of student solutions
3. **Adversarial Robustness** - Test model resilience to subtle perturbations
4. **Chain-of-Thought Analysis** - Study reasoning corruption patterns
5. **Cross-Domain Transfer** - Evaluate generalization across math topics

---

## Data Sources

All problems verified against:
- **AIMO**: Australian Mathematics Trust official solutions
- **AMC**: MAA (Mathematical Association of America) archives
- **AIME**: MAA official answer keys
- **PUMaC**: Princeton University official solutions
- **HMMT**: Harvard-MIT official solutions

---

## License

Dataset released under **CC BY 4.0** for research and educational purposes.

Competition problems remain property of their respective organizations.
