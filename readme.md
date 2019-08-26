# Paperwork - Reference Management Tool For Computer Scientists

![img](https://img.shields.io/badge/version-0.1.0-blue)

Have you ever been frustrated by existing reference management tool? Most CS
papers are published to conferences not journals, while most existing tools
hasn't addressed this problem. There database doesn't provide well access to
CS papers.

**Paperwork** is a reference management tool designed for computer scientists.
It (will) is optimized for CS conferences. Managing your papers and references
hasn't been this easy.

## Requirements

- You need to [download](https://chromedriver.chromium.org) `chromedriver`
  (named as-is) and place it under `res` directory, e.g.,
  ```
  <project_root>/res/chromedriver
  ```
- A running Science Parse server to parse pdf papers. Follow the
  [instructions](https://github.com/allenai/spv2) to run it. You then specify
  its host and port number in the `.env` file, e.g.,
  ```
  sp_host = localhost
  sp_port = 8081
  ```
  For people who has the access to UCLA CS subnet, you don't have to modify it.
  We have a running server specified in this `.env` file.

## TODO

- [] Automatic paper download and file management
- [] `.bibtex` export

## Acknowledgement

- [GROBID](https://github.com/kermitt2/grobid) is a machine learning library for
  extracting, parsing and re-structuring raw documents such as PDF into
  structured XML/TEI encoded documents with a particular focus on technical and
  scientific publications.
- [Science Parse](https://github.com/allenai/science-parse) parses scientific
  papers (in PDF form) and returns them in structured form.
