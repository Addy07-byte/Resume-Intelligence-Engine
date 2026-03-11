# Evaluation

## Goal
Measure whether the generated resume is relevant, accurate, and grounded.

## Metrics

### Keyword Coverage
- Extract keywords from JD
- Check what percentage appear in the generated resume
- Target: >70% coverage

### Faithfulness
- Every claim in the generated resume must be traceable to a retrieved chunk
- No hallucinated responsibilities or skills

## Future Evaluation
- Human evaluation rubric (relevance, readability, accuracy)
- Automated faithfulness scoring using LLM-as-judge