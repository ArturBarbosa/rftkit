# Changelog

All notable changes to RFTKit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-06

### Added
- Core grader base classes (BaseGrader, PythonGrader, ScoreModelGrader, MultiGrader)
- FormattingGrader for JSON structure validation
- IndicatorGrader for cluster-based rubric selection
- RubricGrader for LLM-based evaluation
- AggregatorGrader for weighted score combination
- Cluster-based rubric system with 9 activity format clusters
- Utility functions for grader configuration management
- Comprehensive documentation and examples
- Example Jupyter notebook demonstrating usage

### Fixed
- Typo in sampling parameters (max_completions_tokens -> max_completion_tokens)

## [Unreleased]

### Changed
- **BREAKING**: Default RubricGrader scoring range changed from [0.0, 1.0] to [1, 5] (Likert scale)
- Default pass threshold changed from 0.5 to 3 to align with new 1-5 scale
- Updated rubric grader prompt template to use Likert scale descriptions (1=Strongly Disagree, 5=Strongly Agree)
- Updated all documentation and examples to reflect the new Likert scale

### Planned
- Support for weighted indicators (continuous 0.0-1.0 instead of binary 0/1)
- Dynamic cluster discovery from data patterns
- Hierarchical cluster relationships
- Cross-cluster rubric support with different weights
- Additional example notebooks
- CLI tool for grader configuration management

