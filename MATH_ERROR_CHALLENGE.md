# Break the Chain: Math Error Localization Challenge

## Problem Description

Large language models can solve math problems, but when they make mistakes, it's critical to know **WHERE** in their reasoning the error occurs. This challenge tests error localization in mathematical Chain-of-Thought (CoT) reasoning.

### The Challenge

You are given **242 math problems** from AIMO, AMC, AIME, PUMaC, and HMMT competitions. Each problem includes:
- The problem statement
- A 5-step Chain-of-Thought solution
- The correct final answer

**21% of solutions contain exactly ONE error** at a specific step. Your task is to:
1. Detect IF there is an error (`has_error`: 0 or 1)
2. Identify WHICH STEP contains the error (`error_step`: 1-5)

### Error Types by Step

**Step 1 - wrong_setup**: Incorrectly identifies approach or sets up wrong equation
- Example: "Misapply the quadratic formula" instead of "Apply..."

**Step 2 - wrong_formula**: Applies incorrect formula or theorem
- Example: Uses area formula for wrong shape

**Step 3 - calculation_error**: Makes arithmetic error in calculation
- Example: "15 × 12 = 190" (should be 180)

**Step 4 - logic_error**: Draws wrong conclusion from previous steps
- Example: Invalid deduction from correct premises

**Step 5 - wrong_answer**: States incorrect final answer
- Example: Correct reasoning, wrong final value

### Why This Is Hard

- **Subtle errors**: Errors are minimal perturbations, not obvious mistakes
- **5-class classification**: Must identify exact step (or none)
- **Domain knowledge required**: Algebra, Geometry, Number Theory, Combinatorics, Probability
- **Reasoning verification**: Must trace logical flow across steps

---

## Data Fields

### Identifiers
- `statement_id` (int) - Unique row identifier (0 to N-1)
- `source_id` (string) - Problem ID (e.g., "AMC001", "AIME003")
- `source` (string) - Competition and year (e.g., "AMC 12A 2020")

### Problem Content
- `statement` (string) - The math problem statement
- `domain` (string) - Subject area (Algebra, Geometry, Number Theory, Combinatorics, Probability)
- `correct_answer` (string) - The verified correct answer
- `tier` (int) - Difficulty level (1 = easiest, 4 = hardest)
- `cot` (string) - 5-step Chain-of-Thought reasoning

### Targets (What You Predict)
- `has_error` (int) - **Target 1**: Whether CoT contains an error (0 = correct, 1 = error)
- `error_step` (int) - **Target 2**: Which step has the error (-1 = none, 1-5 = step number)
- `error_type` (string) - Type of error (wrong_setup, wrong_formula, calculation_error, logic_error, wrong_answer, none)

---

## Dataset Statistics

**Total Samples**: 242
**Correct CoT**: 200 (82.6%)
**Error CoT**: 42 (17.4%)
**Base Problems**: 200 unique
**Domains**: 5 (Algebra, Geometry, Number Theory, Combinatorics, Probability)
**Difficulty Tiers**: 4 (Tier 1 = AMC basic, Tier 4 = Olympiad)

### Error Step Distribution
- Step 1: 11 (26.2%)
- Step 2: 10 (23.8%)
- Step 3: 5 (11.9%)
- Step 4: 8 (19.0%)
- Step 5: 8 (19.0%)

### Domain Distribution
- Algebra: ~60 samples
- Geometry: ~50 samples
- Number Theory: ~45 samples
- Combinatorics: ~45 samples
- Probability: ~42 samples

---

## Evaluation

### Primary Metric: Error Detection F1

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)

For binary classification: has_error (0 vs 1)
```

### Secondary Metric: Error Localization Accuracy

```
Accuracy = Correct step predictions / Total error samples

Must predict exact step (1-5) for error samples only
```

### Combined Score

```
Final Score = 0.6 × F1_detection + 0.4 × Accuracy_localization
```

---

## Submission Format

Submit a CSV file:

```csv
statement_id,has_error,predicted_error_step
0,0,-1
1,1,3
2,0,-1
3,1,2
...
```

### Requirements

1. **Format**: CSV with UTF-8 encoding
2. **Header**: `statement_id,has_error,predicted_error_step`
3. **statement_id**: 0 to N-1 matching test set order
4. **has_error**: Binary (0 or 1)
5. **predicted_error_step**: -1 if no error, 1-5 if error detected

---

## Example Data Samples

### CORRECT CoT (No Error)
```
statement_id: 0
statement: "What is the tens digit of 7^2019?"
domain: Mathematics - Number Theory
has_error: 0
error_step: -1
correct_answer: "4"
source: AMC 10A 2019
tier: 3
cot:
Step 1: Find 7^2019 mod 100.
Step 2: Pattern of 7^n mod 100: 7¹=7, 7²=49, 7³=343≡43, 7⁴≡01 (mod 100).
Step 3: Cycle length is 4.
Step 4: Since 2019 = 4×504 + 3, we have 7^2019 ≡ 7³ ≡ 43 (mod 100).
Step 5: The tens digit is 4.

Final Answer: 4
```

### ERROR CoT (Step 4 - Logic Error)
```
statement_id: 1
statement: "In a right triangle, the altitude to the hypotenuse divides it into segments of length 4 and 9. Find the area."
domain: Mathematics - Geometry
has_error: 1
error_step: 4
error_type: logic_error
correct_answer: "39"
source: AIMO 2021
tier: 3
cot:
Step 1: Let the hypotenuse be c = 4 + 9 = 13.
Step 2: By the altitude theorem (geometric mean): h² = 4 × 9 = 36.
Step 3: So the altitude h = 6.
Step 4: Area = (1/2) × base × height = (1/2) × 13 × 6. [LOGIC ERROR]
Step 5: Area = 39 square units.

[ERROR INJECTED AT STEP 4]
```

### ERROR CoT (Step 2 - Wrong Formula)
```
statement_id: 5
statement: "A circle has circumference 16π. What is its area?"
domain: Mathematics - Geometry
has_error: 1
error_step: 2
error_type: wrong_formula
correct_answer: "64π"
source: AMC 10A 2020
tier: 2
cot:
Step 1: Circumference = 2πr = 16π.
Step 2: Solve for r: r = 16π/(2π) = 8. [WRONG FORMULA]
Step 3: Area = πr² = π(8)².
Step 4: Area = 64π.
Step 5: Answer = 64π.

[ERROR INJECTED AT STEP 2]
```

---

## Baseline Approaches

### Rule-Based
- Check each step for arithmetic consistency
- Verify formulas against known identities
- Validate final answer matches given correct_answer

### NLP Models
- Fine-tune BERT/RoBERTa on CoT text with step labels
- Use NLI models to check step-to-step entailment
- Sequence labeling for error position detection

### LLM-Based
- Prompt LLM to verify each step independently
- Use self-consistency: sample multiple verifications
- Tool-augmented: SymPy/calculator for calculation steps

### Multi-Task Learning
```python
# Joint prediction of has_error and error_step
model = MultiTaskModel()
has_error_pred, error_step_pred = model(cot_text)
loss = BCE(has_error) + CrossEntropy(error_step)
```

---

## Getting Started

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

# Load data
df = pd.read_csv('math_error_localization_v2.csv')

# Split
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Baseline 1: Predict all correct (F1 = 0 for error class)
y_pred_error = [0] * len(test)
f1 = f1_score(test['has_error'], y_pred_error, pos_label=1)
print(f"Baseline F1 (all correct): {f1:.4f}")

# Baseline 2: Random step prediction for errors
import random
y_pred_step = [random.randint(1, 5) if y == 1 else -1
               for y in test['has_error']]
error_mask = test['has_error'] == 1
acc = accuracy_score(test.loc[error_mask, 'error_step'],
                     [y_pred_step[i] for i in range(len(test)) if error_mask.iloc[i]])
print(f"Random localization accuracy: {acc:.4f}")

# Your model here
# has_error_pred, error_step_pred = model.predict(test['cot'])
```

---

## Research Applications

1. **LLM Self-Correction** - Help models identify their own reasoning errors
2. **Educational Tools** - Automated feedback on student problem-solving steps
3. **Formal Verification** - Bridge between neural and symbolic reasoning
4. **Uncertainty Quantification** - Detect low-confidence reasoning steps
5. **Step-wise Reward Modeling** - Fine-grained RLHF for mathematical reasoning

---

## Data Sources

All problem statements and final answers verified against:
- **AIMO**: Australian Mathematics Trust
- **AMC**: Mathematical Association of America (MAA)
- **AIME**: MAA Official Answer Keys
- **PUMaC**: Princeton University
- **HMMT**: Harvard-MIT

**Chain-of-Thought**: Generated programmatically, NOT copied from any source.

---

## License

Dataset released under **CC BY 4.0** for research and educational purposes.

Competition problems remain property of their respective organizations.
