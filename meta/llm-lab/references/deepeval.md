# DeepEval — Configuration reference

## Role in the lab

DeepEval objectively measures the quality of a skill on a given model.
It lets you compare how different LLMs perform on the same tasks
and catch regressions in CI/CD.

## Installation

```bash
pip install deepeval
# or in a dedicated venv
python -m venv ~/llm-lab/evals/.venv
source ~/llm-lab/evals/.venv/bin/activate
pip install deepeval openai  # openai SDK to call LiteLLM
```

## Configuration

DeepEval uses an LLM as a judge (LLM-as-judge). Point it at LiteLLM
to use any model as the evaluator.

```python
# evals/conftest.py
import os
os.environ["OPENAI_API_KEY"] = "sk-master-CHANGE-ME"
os.environ["OPENAI_API_BASE"] = "http://localhost:4000/v1"
```

## Test structure

```
~/llm-lab/evals/
├── conftest.py              # Shared config (LiteLLM endpoint)
├── test_senior_dev.py       # Tests for the senior-dev skill
├── test_documentor.py       # Tests for the documentor skill
├── datasets/
│   ├── senior_dev_cases.json  # Test cases with input/expected
│   └── documentor_cases.json
└── results/
    └── benchmark_2026-04-21.json
```

## Writing a skill test

```python
# evals/test_senior_dev.py
import pytest
from openai import OpenAI
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval, AnswerRelevancyMetric

# Client pointing at LiteLLM
client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="sk-master-CHANGE-ME"
)

# Metrics
relevancy = AnswerRelevancyMetric(threshold=0.7)
quality = GEval(
    name="Skill Instruction Following",
    criteria="The output follows the skill's instructions precisely, "
             "is well-structured, actionable, and production-ready.",
    evaluation_params=["input", "actual_output"],
    threshold=0.7
)

MODELS = ["qwen3-8b", "qwen3-72b", "claude-sonnet"]

SKILL_PROMPT = """You are a senior dev. Analyze this problem and propose
options with trade-offs."""

TEST_CASES = [
    {
        "input": "We need to choose between PostgreSQL and MongoDB for our e-commerce orders API.",
        "expected": "At least 2 options with explicit trade-offs and a recommendation"
    },
    {
        "input": "Our API takes 3s to respond on the /search endpoint. How do we diagnose it?",
        "expected": "A structured diagnostic approach, no premature solution"
    }
]


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("case", TEST_CASES)
def test_skill_quality(model, case):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SKILL_PROMPT},
            {"role": "user", "content": case["input"]}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    output = response.choices[0].message.content
    
    test_case = LLMTestCase(
        input=case["input"],
        actual_output=output,
        expected_output=case["expected"]
    )
    
    assert_test(test_case, [relevancy, quality])
```

## Useful metrics for your skills

| Metric | Usage |
|--------|-------|
| `GEval` | Custom evaluation against any criterion (the most flexible) |
| `AnswerRelevancyMetric` | Is the answer relevant to the input? |
| `FaithfulnessMetric` | Is the answer faithful to the provided context? (RAG) |
| `HallucinationMetric` | Detects factual hallucinations |
| `BiasMetric` | Detects bias in the answer |
| `ToxicityMetric` | Detects toxic content |

### Custom metrics (GEval)

```python
# Example: evaluate whether a documentor skill cites its sources
source_citation = GEval(
    name="Source Citation Quality",
    criteria="Every factual claim in the output is backed by an inline "
             "source citation. Sources are real and verifiable.",
    evaluation_params=["actual_output"],
    threshold=0.8
)
```

## Running the tests

```bash
# All tests
cd ~/llm-lab/evals
deepeval test run test_senior_dev.py

# A single model
deepeval test run test_senior_dev.py -k "qwen3-72b"

# Verbose
deepeval test run test_senior_dev.py -v

# Generate a report
deepeval test run test_senior_dev.py --json-output results/report.json
```

## CI/CD integration (GitHub Actions)

```yaml
# .github/workflows/llm-evals.yml
name: LLM Quality Evals
on:
  push:
    paths:
      - 'skills/**'
      - 'evals/**'

jobs:
  eval:
    runs-on: self-hosted  # On the Mac Studio
    steps:
      - uses: actions/checkout@v4
      - name: Run evals
        run: |
          cd evals
          deepeval test run . --json-output results/report.json
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: evals/results/
```

## Interpreting the results

A DeepEval score is between 0 and 1. The threshold defines pass/fail.

| Score | Interpretation |
|-------|----------------|
| > 0.8 | Excellent — model viable for this skill |
| 0.6 - 0.8 | Acceptable — usable with supervision |
| < 0.6 | Insufficient — switch models or adapt the skill |

To compare models, run the same test on each and compare the scores.
A "cheaper" model (local 8B) that scores > 0.7 on a skill is preferable
to a cloud model that scores 0.9 but costs 100× more.
