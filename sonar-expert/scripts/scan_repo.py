#!/usr/bin/env python3
"""Deterministic repository scanner for the sonar-expert skill.

The script inspects a repository without modifying it and emits JSON that helps
an agent choose an appropriate SonarQube configuration.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".cache",
    ".turbo",
    ".next",
    ".nuxt",
    ".output",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "bower_components",
    "dist",
    "build",
    "target",
    "out",
    "coverage",
    ".terraform",
    "vendor",
}

LANG_BY_EXT = {
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".py": "python",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".h": "c_cpp",
    ".cc": "c_cpp",
    ".cpp": "c_cpp",
    ".cxx": "c_cpp",
    ".hpp": "c_cpp",
    ".hxx": "c_cpp",
    ".swift": "swift",
    ".php": "php",
    ".rb": "ruby",
    ".scala": "scala",
    ".tf": "terraform",
    ".tfvars": "terraform",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".xml": "xml",
    ".sql": "sql",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".ps1": "powershell",
    ".Dockerfile": "docker",
}

MARKERS = {
    "package_json": ["package.json"],
    "pnpm_workspace": ["pnpm-workspace.yaml"],
    "turbo": ["turbo.json"],
    "nx": ["nx.json"],
    "pyproject": ["pyproject.toml"],
    "requirements": ["requirements.txt", "requirements-dev.txt"],
    "poetry_lock": ["poetry.lock"],
    "uv_lock": ["uv.lock"],
    "maven": ["pom.xml"],
    "gradle": ["build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"],
    "dotnet": [".sln", ".csproj"],
    "go_mod": ["go.mod"],
    "cargo": ["Cargo.toml"],
    "sonar": ["sonar-project.properties", ".sonarcloud.properties"],
    "jenkins": ["Jenkinsfile"],
    "github_actions": [".github/workflows"],
    "gitlab_ci": [".gitlab-ci.yml"],
    "azure_pipelines": ["azure-pipelines.yml"],
    "docker": ["Dockerfile", "docker-compose.yml", "compose.yml", "compose.yaml"],
    "terraform": [".tf"],
    "helm": ["Chart.yaml"],
    "ansible": ["ansible.cfg", "playbook.yml", "playbooks"],
}

COVERAGE_MARKERS = {
    "lcov": ["coverage/lcov.info", "lcov.info"],
    "python_coverage_xml": ["coverage.xml"],
    "jacoco": ["target/site/jacoco/jacoco.xml", "build/reports/jacoco/test/jacocoTestReport.xml"],
    "opencover": ["coverage.opencover.xml"],
    "vstest": ["TestResults"],
    "go_coverage": ["coverage.out"],
    "cobertura": ["coverage/cobertura-coverage.xml", "cobertura.xml"],
}

TEST_PATTERNS = (
    "__tests__",
    "/tests/",
    "/test/",
    ".test.",
    ".spec.",
    "_test.go",
    "Test.cs",
    "Tests.cs",
)

GENERATED_HINTS = (
    "generated",
    "__generated__",
    ".generated.",
    "openapi",
    "swagger",
    "graphql",
    "pb.go",
    ".pb.",
)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def should_skip_dir(path: Path) -> bool:
    return path.name in SKIP_DIRS


def iter_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for current_root, dirnames, filenames in os.walk(root):
        current = Path(current_root)
        dirnames[:] = sorted(d for d in dirnames if not should_skip_dir(current / d))
        for filename in sorted(filenames):
            if len(files) >= max_files:
                return files
            files.append(current / filename)
    return files


def language_for(path: Path) -> str | None:
    if path.name == "Dockerfile" or path.name.endswith(".Dockerfile"):
        return "docker"
    return LANG_BY_EXT.get(path.suffix)


def marker_matches(path: Path, root: Path) -> list[str]:
    relative = rel(path, root)
    found: list[str] = []
    for marker, patterns in MARKERS.items():
        for pattern in patterns:
            if pattern.startswith(".") and path.suffix == pattern:
                found.append(marker)
            elif pattern.startswith(".") and relative.endswith(pattern):
                found.append(marker)
            elif "/" in pattern and relative.startswith(pattern):
                found.append(marker)
            elif path.name == pattern:
                found.append(marker)
    return found


def detect_monorepo(files: list[Path], root: Path, markers: dict[str, list[str]]) -> dict[str, Any]:
    candidates: set[str] = set()
    for path in files:
        relative = rel(path, root)
        parts = relative.split("/")
        if len(parts) >= 3 and parts[0] in {"apps", "packages", "services", "libs", "modules"}:
            candidates.add("/".join(parts[:2]))
        if path.name in {"package.json", "pyproject.toml", "pom.xml", "go.mod", "Cargo.toml"} and path.parent != root:
            parent = rel(path.parent, root)
            if parent != ".":
                candidates.add(parent)
    return {
        "is_monorepo": bool(markers.get("pnpm_workspace") or markers.get("turbo") or markers.get("nx") or len(candidates) >= 2),
        "modules": sorted(candidates)[:80],
    }


def infer_profiles(markers: dict[str, list[str]], languages: Counter[str], monorepo: dict[str, Any], files_rel: list[str]) -> list[str]:
    profiles: set[str] = set()
    if languages.get("typescript") or languages.get("javascript"):
        profiles.add("web-saas" if any(p.startswith(("src/", "app/", "pages/", "components/")) for p in files_rel) else "backend-api")
    if any(languages.get(lang) for lang in ["python", "java", "go", "csharp", "kotlin", "php", "ruby"]):
        profiles.add("backend-api")
    if monorepo["is_monorepo"]:
        profiles.add("monorepo-platform")
    if markers.get("terraform") or markers.get("helm") or markers.get("ansible") or markers.get("docker"):
        profiles.add("infra-iac")
    if any(languages.get(lang) for lang in ["c", "c_cpp"]):
        profiles.add("mission-critical")
    if any("legacy" in p.lower() for p in files_rel) or not any("coverage" in p.lower() for p in files_rel):
        profiles.add("legacy-cleanup")
    ai_markers = {"ai", "llm", "llms", "openai", "anthropic", "gemini"}
    for relative in files_rel:
        tokens = {
            token
            for part in Path(relative.lower()).parts
            for token in part.replace("_", "-").replace(".", "-").split("-")
            if token
        }
        if tokens & ai_markers:
            profiles.add("ai-assisted-code")
            break
    return sorted(profiles)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a repository for SonarQube configuration signals.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository root to scan")
    parser.add_argument("--max-files", type=int, default=12000, help="Maximum number of files to inspect")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    files = iter_files(root, args.max_files)
    files_rel = [rel(path, root) for path in files]
    language_counts: Counter[str] = Counter()
    extensions: Counter[str] = Counter()
    markers: dict[str, list[str]] = defaultdict(list)
    tests: list[str] = []
    generated: list[str] = []
    coverage: dict[str, list[str]] = defaultdict(list)

    for path in files:
        relative = rel(path, root)
        language = language_for(path)
        if language:
            language_counts[language] += 1
        if path.suffix:
            extensions[path.suffix] += 1
        for marker in marker_matches(path, root):
            markers[marker].append(relative)
        normalized = f"/{relative}"
        if any(pattern in normalized for pattern in TEST_PATTERNS):
            tests.append(relative)
        lowered = relative.lower()
        if any(hint in lowered for hint in GENERATED_HINTS):
            generated.append(relative)
        for cov_name, cov_patterns in COVERAGE_MARKERS.items():
            if any(relative == pattern or relative.endswith(f"/{pattern}") or relative.startswith(pattern) for pattern in cov_patterns):
                coverage[cov_name].append(relative)

    monorepo = detect_monorepo(files, root, markers)
    profiles = infer_profiles(markers, language_counts, monorepo, files_rel)
    dominant_languages = [lang for lang, _ in language_counts.most_common(8)]

    result = {
        "repo_root": str(root),
        "file_count_scanned": len(files),
        "truncated": len(files) >= args.max_files,
        "dominant_languages": dominant_languages,
        "language_file_counts": dict(language_counts.most_common()),
        "top_extensions": dict(extensions.most_common(20)),
        "markers": {key: sorted(set(value))[:80] for key, value in sorted(markers.items())},
        "monorepo": monorepo,
        "inferred_project_profiles": profiles,
        "tests_detected": sorted(tests)[:120],
        "coverage_artifacts": {key: sorted(set(value)) for key, value in sorted(coverage.items())},
        "generated_or_vendor_hints": sorted(generated)[:120],
        "recommended_template_refs": recommend_templates(dominant_languages, profiles),
        "notes": [
            "This scanner is deterministic and read-only.",
            "Review inferred profiles before writing SonarQube configuration.",
            "Do not treat missing coverage artifacts as proof that tests do not exist; inspect test scripts too.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def recommend_templates(languages: list[str], profiles: list[str]) -> list[str]:
    refs: list[str] = []
    if any(lang in languages for lang in ["typescript", "javascript"]):
        refs.append("references/templates/typescript.md")
    if "python" in languages:
        refs.append("references/templates/python.md")
    if "java" in languages or "kotlin" in languages:
        refs.append("references/templates/java.md")
    if "go" in languages:
        refs.append("references/templates/go.md")
    if "csharp" in languages:
        refs.append("references/templates/dotnet.md")
    if any(lang in languages for lang in ["c", "c_cpp"]):
        refs.append("references/templates/cpp.md")
    if "infra-iac" in profiles:
        refs.append("references/templates/iac.md")
    if "monorepo-platform" in profiles:
        refs.append("references/templates/monorepo.md")
    return refs


if __name__ == "__main__":
    raise SystemExit(main())
