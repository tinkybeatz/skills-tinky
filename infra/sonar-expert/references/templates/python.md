# SonarQube Template — Python

Use when the scanner detects `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`, or Python source files.

## Project scope

```properties
sonar.sources=src,app,services
sonar.tests=tests
sonar.test.inclusions=tests/**/*.py,**/test_*.py,**/*_test.py
sonar.sourceEncoding=UTF-8
```

For flat repos, `sonar.sources=.` is acceptable only after excluding virtualenvs, generated files, build output and coverage artifacts.

## Coverage

Prefer Coverage.py XML output:

```properties
sonar.python.coverage.reportPaths=coverage.xml
```

Typical command:

```bash
pytest --cov=src --cov-report=xml
```

Adapt `--cov` to the real source package. If no coverage exists, configure Sonar without fake coverage and list the command needed to generate `coverage.xml`.

## Exclusions

```properties
sonar.exclusions=**/.venv/**,**/venv/**,**/.tox/**,**/__pycache__/**,**/.pytest_cache/**,**/.mypy_cache/**,**/.ruff_cache/**,**/build/**,**/dist/**,**/coverage/**,**/generated/**,**/*_pb2.py,**/*_pb2_grpc.py
sonar.coverage.exclusions=**/tests/**,**/test_*.py,**/*_test.py,**/migrations/**,**/settings.py,**/config.py,**/generated/**,**/*_pb2.py,**/*_pb2_grpc.py
sonar.cpd.exclusions=**/migrations/**,**/fixtures/**,**/generated/**,**/*_pb2.py,**/*_pb2_grpc.py
```

Do not exclude application modules because they are hard to test; classify that as legacy debt.

## Quality profile

- Start with `Sonar way` for Python.
- Keep Ruff, mypy/pyright and framework-specific validators as complementary CI checks.
- Consider stricter security review for services handling user input, files, subprocesses, SQL, auth or secrets.

## Quality gate

- Default: `standard-app` for maintained code.
- For legacy without coverage: strict new-code gate, coverage target only after coverage generation is in place.
- Security hotspots must be reviewed, not ignored.

