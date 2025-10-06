# Cluster-Based Rubric Evaluation System

## Overview

The cluster-based rubric approach is a key feature of RFTKit that enables **efficient and precise evaluation** by ensuring that each activity format is only evaluated against relevant criteria.

## Concept

In traditional evaluation systems, all rubrics are applied to all activities, leading to:
- Wasted computation on irrelevant criteria
- Diluted scores from non-applicable rubrics
- Difficulty in interpreting results

The cluster-based approach solves this by:
1. **Grouping** activity formats into clusters (e.g., ChatIntroduceLexis, VideoIntroduceGrammar)
2. **Defining** specific rubric sets for each cluster
3. **Filtering** rubrics at evaluation time using IndicatorGraders
4. **Aggregating** only relevant rubric scores

## How It Works

### 1. Activity Type Detection

When an activity is evaluated, the system first identifies its type:

```python
activity_type = extract_format_from_content(activity)
# e.g., "ChatIntroduceLexisTeacher"
```

### 2. Indicator Grader Filtering

Each rubric has a corresponding IndicatorGrader that returns:
- `1.0` if the rubric applies to this activity type
- `0.0` if the rubric doesn't apply

```python
def grade(sample, item):
    activity_type = detect_activity_type(sample)
    valid_rubrics = cluster_map[activity_type]
    
    if rubric_name in valid_rubrics:
        return 1.0  # Rubric applies
    else:
        return 0.0  # Rubric doesn't apply
```

### 3. Score Aggregation

The final score uses multiplicative masking:

```
Final = Format_Score + Σ(Indicator[i] × Weight[i] × Rubric_Score[i])
```

When Indicator = 0, that term becomes 0, effectively excluding the rubric.

## Example

### Cluster Definition

```python
{
    "ChatIntroduceLexisTeacher": [
        "active_participation",
        "lexical_input_quality",
        "tone_and_engagement"
    ],
    "VideoIntroduceGrammarClassroom": [
        "opening_and_contextualization",
        "noticing_and_implicit_contrast",
        "progression_and_scaffolding"
    ]
}
```

### Evaluation Flow

For a `ChatIntroduceLexisTeacher` activity:

1. Format validation: Always evaluated (1.0 or 0.0)
2. Rubric "active_participation": 
   - Indicator = 1.0 (applies to this cluster)
   - Rubric score = 0.85
   - Contribution = 1.0 × 1.0 × 0.85 = 0.85
3. Rubric "opening_and_contextualization":
   - Indicator = 0.0 (doesn't apply to this cluster)
   - Rubric score = 0.92 (calculated but not used)
   - Contribution = 0.0 × 1.0 × 0.92 = 0.0

## Benefits

### 1. Precision
Each activity type gets evaluated only on criteria that matter for its specific purpose.

### 2. Efficiency
No wasted LLM calls on irrelevant rubrics (though indicator graders still run, they're fast Python code).

### 3. Scalability
Easy to add new clusters by defining their rubric sets.

### 4. Interpretability
Clear mapping between activity purposes and evaluation criteria.

## Implementation

### Step 1: Define Clusters

In `indicator_validator.py`, define your cluster mapping:

```python
activity_type_to_rubric_item_map = {
    "YourActivityType": [
        "rubric_1",
        "rubric_2",
        # ... up to 8-10 rubrics
    ]
}
```

### Step 2: Create Graders

```python
# For each rubric in ALL clusters
rubric_graders = []
indicator_graders = []

for rubric_name in all_rubrics:
    # Create rubric grader
    rubric_grader = RubricGrader(
        name=f"rubric_{rubric_name}",
        rubric=rubrics[rubric_name],
        weight=1.0
    )
    rubric_graders.append(rubric_grader)
    
    # Create indicator grader
    indicator = IndicatorGrader(
        name=f"indicator_{rubric_name}",
        rubric_name=rubric_name
    )
    indicator_graders.append(indicator)
```

### Step 3: Aggregate

```python
aggregator = AggregatorGrader(
    name="final_score",
    graders=[format_grader] + rubric_graders + indicator_graders,
    rubric_to_indicator_map={
        f"rubric_{name}": f"indicator_{name}" 
        for name in all_rubrics
    },
    formatting_grader_name="format"
)
```

## Current Implementation Stats

- **9 Clusters** (Activity Formats)
- **49 Total Rubrics** (Across all clusters)
- **~8 Rubrics per Cluster** (Carefully selected)
- **Binary Indicator System** (0 or 1 activation)

## Future Enhancements

### 1. Weighted Indicators
Instead of binary (0/1), use continuous weights (0.0-1.0) for partial relevance:

```python
# Rubric is highly relevant
indicator = 1.0

# Rubric is somewhat relevant
indicator = 0.5

# Rubric is not relevant
indicator = 0.0
```

### 2. Dynamic Clustering
Automatically discover clusters from data patterns using ML:

```python
clusters = discover_clusters(activity_data)
rubric_mapping = assign_rubrics_to_clusters(clusters, rubrics)
```

### 3. Hierarchical Clusters
Parent-child relationships between activity types:

```
ChatActivities (parent)
├── ChatIntroduceLexis (child)
└── ChatConsolidateLexis (child)
```

Shared rubrics at parent level, specific ones at child level.

### 4. Cross-Cluster Rubrics
Some rubrics could apply with different weights across clusters:

```python
{
    "rubric_engagement": {
        "ChatIntroduceLexis": 1.0,
        "VideoIntroduceGrammar": 0.7,
        "ChatTestPronunciation": 0.5
    }
}
```

## Best Practices

### 1. Cluster Cohesion
Keep clusters focused on similar activity types with shared characteristics.

### 2. Rubric Selection
Choose 8-10 rubrics per cluster that are:
- Specific to the cluster's purpose
- Measurable with clear criteria
- Non-overlapping with each other

### 3. Regular Review
Periodically review cluster assignments and rubric relevance based on:
- Model performance
- Evaluation results
- User feedback

### 4. Documentation
Maintain clear documentation of:
- Why each cluster exists
- What makes rubrics relevant to each cluster
- Examples of activities in each cluster

## Conclusion

The cluster-based rubric system is a powerful approach for managing complex, multi-dimensional evaluation criteria across diverse activity types. By filtering rubrics at evaluation time, it ensures efficient, precise, and interpretable assessments.

