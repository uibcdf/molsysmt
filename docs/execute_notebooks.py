#!/usr/bin/env python

import os
import sys
import json
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timezone
import argparse
from concurrent.futures import ThreadPoolExecutor

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Log file in the same directory as this script, listing notebooks that failed.
ERROR_LOG_PATH = Path(__file__).resolve().with_name("notebook_errors.log")

def write_timestamp_to_log(log_path: Path, quiet: bool = False):
    timestamp = datetime.now(timezone.utc).timestamp()
    log_path.write_text(f"{timestamp:.6f}")
    if not quiet:
        print(f"Timestamp written to {log_path}: {timestamp:.6f}")
    return timestamp

def read_timestamp_from_log(log_path: Path) -> float:
    try:
        return float(log_path.read_text().strip())
    except Exception:
        return 0.0

def get_git_status_uncommitted(notebook_path: Path) -> bool:
    """Check if notebook has uncommitted local changes (modified, untracked, or staged) in Git."""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain", str(notebook_path)],
            capture_output=True,
            text=True,
            check=False
        )
        return bool(res.stdout.strip())
    except Exception:
        return True

def get_git_last_commit_time(notebook_path: Path) -> float:
    """Get UTC timestamp of last Git commit for notebook_path."""
    try:
        res = subprocess.run(
            ["git", "log", "-1", "--format=%ct", str(notebook_path)],
            capture_output=True,
            text=True,
            check=False
        )
        val = res.stdout.strip()
        return float(val) if val else 0.0
    except Exception:
        return 0.0

def sanitize_notebook_outputs(notebook_path: Path) -> bool:
    """Ensure every code cell in notebook JSON schema has an 'outputs' list to prevent myst_nb crashes."""
    try:
        content = notebook_path.read_text(encoding="utf-8")
        data = json.loads(content)
        modified = False
        if "cells" in data and isinstance(data["cells"], list):
            for cell in data["cells"]:
                if cell.get("cell_type") == "code":
                    if "outputs" not in cell or not isinstance(cell["outputs"], list):
                        cell["outputs"] = []
                        modified = True
        if modified:
            notebook_path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return True
    except Exception as e:
        print(f"Warning: could not sanitize notebook schema for {notebook_path}: {e}")
        return False

def execute_notebook(notebook_path: Path, force: bool = False, quiet: bool = False, progress_tracker = None) -> bool:

    last_run_file = notebook_path.with_suffix('.nbconvert.last_run')
    log_file = notebook_path.with_suffix('.nbconvert.log')

    needs_execution = False

    if last_run_file.exists():
        last_run_time = read_timestamp_from_log(last_run_file)
        is_uncommitted = get_git_status_uncommitted(notebook_path)

        if is_uncommitted:
            # Active local session modification (tracked modified or untracked)
            notebook_time = notebook_path.stat().st_mtime
            if notebook_time > last_run_time:
                needs_execution = True
        else:
            # Clean in Git status (e.g. fresh clone / branch checkout)
            commit_time = get_git_last_commit_time(notebook_path)
            if commit_time > last_run_time:
                needs_execution = True
    else:
        needs_execution = True

    if needs_execution or force:

        if not quiet:
            print(f"Executing notebook: {notebook_path}")
        env["MSM_VIEWS_FROM_HTML_FILES"] = "True"
        env["MSM_DOCS_NOTEBOOK"] = str(notebook_path)

        result = subprocess.run(
            ["jupyter", "nbconvert", "--execute", "--inplace", str(notebook_path)],
            capture_output=True,
            text=True,
            env=env
        )

        log_file.write_text(result.stdout + "\n" + result.stderr)

        if result.returncode != 0:
            print(f"{RED}✘{RESET} Error executing {notebook_path}: check {log_file}")
            if last_run_file.exists():
                last_run_file.unlink()
            try:
                with ERROR_LOG_PATH.open("a", encoding="utf-8") as f:
                    f.write(f"{notebook_path}\n")
            except Exception:
                pass
            if progress_tracker:
                progress_tracker.update(executed=True, failed=True, notebook_path=notebook_path)
            return False
        else:
            sanitize_notebook_outputs(notebook_path)
            write_timestamp_to_log(last_run_file, quiet=True)
            if progress_tracker:
                progress_tracker.update(executed=True, notebook_path=notebook_path)
            elif not quiet:
                print(f"{GREEN}✔{RESET} Notebook {notebook_path} executed successfully.")
            return True

    else:
        sanitize_notebook_outputs(notebook_path)
        if progress_tracker:
            progress_tracker.update(executed=False)
        elif not quiet:
            print(f"{BLUE}●{RESET} Notebook {notebook_path} is up to date. No execution needed.")
        return True


class ProgressTracker:
    """Milestone and time-based progress emitter inspired by pytest-receptor."""

    def __init__(self, total: int, quiet: bool, step_percent: int = 20):
        self.total = total
        self.quiet = quiet
        self.step_percent = step_percent
        self.completed = 0
        self.executed = 0
        self.failed = 0
        self.start_time = time.monotonic()
        self.next_threshold = step_percent
        self.lock = threading.Lock()

    def update(self, executed: bool, failed: bool = False, notebook_path: Path = None):
        with self.lock:
            self.completed += 1
            if executed:
                self.executed += 1
            if failed:
                self.failed += 1

            if self.quiet and self.total > 0:
                elapsed = time.monotonic() - self.start_time
                percent = (self.completed * 100) // self.total

                # Emit milestone line at percentage threshold boundaries (e.g. 20%, 40%, 60%, 80%)
                if percent >= self.next_threshold and self.completed < self.total:
                    sys.stderr.write(f"execute_notebooks: {percent}% {self.completed}/{self.total} ({elapsed:.0f}s)\n")
                    sys.stderr.flush()
                    self.next_threshold = (percent // self.step_percent + 1) * self.step_percent


def main(force=False, notebook: Path = None, recursive: bool = False, n_workers: int = 1, quiet: bool = False):

    if notebook is not None:
        if not notebook.exists():
            print(f"{RED}✘{RESET} {notebook} does not exist.")
            return
        if notebook.is_file():
            nb_list = [notebook]
        elif notebook.is_dir():
            if recursive:
                nb_list = list(notebook.rglob("*.ipynb"))
            else:
                nb_list = list(notebook.glob("*.ipynb"))
    else:
        if recursive:
            nb_list = list(Path(".").rglob("*.ipynb"))
        else:
            nb_list = list(Path(".").glob("*.ipynb"))

    nb_list = [nb for nb in nb_list if ".ipynb_checkpoints" not in nb.parts]
    total_nbs = len(nb_list)

    n_workers = max(1, int(n_workers) if n_workers is not None else 1)

    start_time = time.monotonic()
    if quiet:
        sys.stderr.write(f"execute_notebooks: starting {total_nbs} notebooks using {n_workers} workers...\n")
        sys.stderr.flush()

    progress_tracker = ProgressTracker(total_nbs, quiet)
    failed_notebooks = []

    if n_workers == 1:
        for nb_path in nb_list:
            try:
                ok = execute_notebook(nb_path, force, quiet=quiet, progress_tracker=progress_tracker)
            except Exception:
                ok = False
                try:
                    with ERROR_LOG_PATH.open("a", encoding="utf-8") as f:
                        f.write(f"{nb_path}\n")
                except Exception:
                    pass
            if not ok:
                failed_notebooks.append(nb_path)
    else:
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            future_to_nb = {
                executor.submit(execute_notebook, nb_path, force, quiet, progress_tracker): nb_path
                for nb_path in nb_list
            }
            for future, nb_path in future_to_nb.items():
                try:
                    ok = future.result()
                except Exception:
                    ok = False
                    try:
                        with ERROR_LOG_PATH.open("a", encoding="utf-8") as f:
                            f.write(f"{nb_path}\n")
                    except Exception:
                        pass
                if not ok:
                    failed_notebooks.append(nb_path)

    elapsed = time.monotonic() - start_time
    executed = progress_tracker.executed
    skipped = total_nbs - executed

    if failed_notebooks:
        print(f"{RED}✘{RESET} {len(failed_notebooks)} notebook(s) failed in {elapsed:.1f}s. "
              f"See {ERROR_LOG_PATH}")
    else:
        if quiet:
            sys.stderr.write(f"execute_notebooks: 100% {total_nbs}/{total_nbs} ({elapsed:.1f}s)\n")
            sys.stderr.flush()
        print(f"{GREEN}✔{RESET} All {total_nbs} notebook(s) processed cleanly in {elapsed:.1f}s ({executed} executed, {skipped} up to date).")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="""
    Execute Jupyter notebooks if they have been modified since their last successful execution.
    You can pass a single notebook path, a directory, or a wildcard pattern (e.g. '*.ipynb').
    
    Examples:
        python execute_notebooks.py                       # All notebooks in current directory
        python execute_notebooks.py -q -r                 # Quiet milestone progress mode (inspired by pytest-receptor)
        python execute_notebooks.py -n 4 -r               # Recursively using 4 workers in parallel
        python execute_notebooks.py -r docs/user_guide    # All notebooks in docs/user_guide recursively
        python execute_notebooks.py analysis.ipynb        # Only that notebook
        python execute_notebooks.py -f                    # Force re-execution of all
        python execute_notebooks.py -fr docs/user_guide   # Combine flags: force + recursive
    
    Each successful run updates a corresponding .nbconvert.last_run file with a timestamp.
    Notebooks are skipped if unchanged.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("notebook", nargs="*", default=None,
                        help="Notebook(s) to execute. Supports wildcard patterns (e.g. *.ipynb).")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force execution of notebooks regardless of timestamps.")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Search for notebooks recursively in directories.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Quiet mode: emit milestone percentage/time lines (pytest-receptor style); print errors and summary only.")
    parser.add_argument(
        "-n", "--n-workers", type=int, default=1,
        help="Number of worker threads to use for notebook execution. "
             "Use 1 (default) to run serially without parallel workers."
    )

    args = parser.parse_args()

    # Reset error log at the beginning of a CLI invocation.
    try:
        ERROR_LOG_PATH.write_text("", encoding="utf-8")
    except Exception:
        pass

    if args.notebook:
        for nb in map(Path, args.notebook):
            if nb.is_file():
                main(force=args.force, notebook=nb, recursive=args.recursive, n_workers=args.n_workers, quiet=args.quiet)
            elif nb.is_dir():
                main(force=args.force, notebook=nb, recursive=args.recursive, n_workers=args.n_workers, quiet=args.quiet)
            else:
                print(f"{RED}✘{RESET} File not found or not a notebook: {nb}")
    else:
        main(force=args.force, recursive=args.recursive, n_workers=args.n_workers, quiet=args.quiet)
