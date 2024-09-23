# ScrapeAI
Simple Python wrapper that pulls desired information from a collection of documents using Anthropic's API.

# Motivation
The main imagined use case is having a simple way of getting the same piece of information from a collection of similar documents. For example, getting a list of training data sources, author info, algorithm details, or relevant citations from ten research papers.

# Installation
Clone repo and `pip install -e .`.

# Usage

```python
from scrapeai import Folder

# Specify collection of PDFs.
folder = Folder(path='./path/to/folder', files_endwith=['.pdf'])

# Print files in collection.
print(folder.files)
# ['machine_learning_paper_189.pdf', 'transformer_paper_193.pdf', ...]

# Get information from each file in collection.
answer = folder.ask('How was the model trained?')

print(answer)

# [('machine_learning_paper_189.pdf', 'Trained using XYZ'), ('transformer_paper_193.pdf', 'Trained using WYX'), ...]

answer = folder.ask('Which data sources were used for training?')

print(answer)

# [('machine_learning_paper_189.pdf', 'Used CFAR1000'), ('transformer_paper_193.pdf', 'Used self-labeled cats'), ...]
```
