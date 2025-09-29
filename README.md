# **RFTKit**: A Python toolkit for OpenAI's Reinforcement Fine-Tuning.

RFTKit is a comprehensive Python toolkit designed to streamline the implementation of [OpenAI's **Reinforcement Fine-Tuning (RFT)**](https://platform.openai.com/docs/guides/reinforcement-fine-tuning) workflow. It facilitates creating custom graders by providing an easy-to-use and extensible, serializable Pydantic-based API. The toolkit also serves as an SDK for [OpenAI's **Graders API**](https://platform.openai.com/docs/api-reference/graders) and a collection of utilities for efficiently working with training and validation datasets in RFT workflows.

## Installation

RFTKit is supported on Python 3.12+. The recommended way to install RFTKit is via [pip](https://pypi.python.org/pypi/pip).

```
pip install rftkit
```

You can then import the library in code:

```
import rftkit
# or
import rftkit as rft
```

