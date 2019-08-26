# Dunder Mifflin

![logo](res/logo.jpg)

Dunder Mifflin is a paper repository, containing all good papers we love.

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
