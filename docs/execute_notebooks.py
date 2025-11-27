#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import argparse
import glob
from concurrent.futures import ThreadPoolExecutor

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Log file in the same directory as this script, listing notebooks that failed.
ERROR_LOG_PATH = Path(__file__).resolve().with_name("notebook_errors.log")

def write_timestamp_to_log(log_path: Path):
    timestamp = datetime.now(timezone.utc).timestamp()
    log_path.write_text(f"{timestamp:.6f}")
    print(f"Timestamp written to {log_path}: {timestamp:.6f}")
    return timestamp

def read_timestamp_from_log(log_path: Path) -> float:
    try:
        return float(log_path.read_text().strip())
    except Exception:
        return 0.0

def execute_notebook(notebook_path: Path, force: bool = False) -> bool:

    last_run_file = notebook_path.with_suffix('.nbconvert.last_run')
    log_file = notebook_path.with_suffix('.nbconvert.log')

    needs_execution = False

    if last_run_file.exists():
        last_run_time = read_timestamp_from_log(last_run_file)
        notebook_time = notebook_path.stat().st_mtime
        if notebook_time > last_run_time:
            needs_execution = True
    else:
        needs_execution = True

    if needs_execution or force:

        print(f"Executing notebook: {notebook_path}")
        env = os.environ.copy()
        env["MSM_VIEWS_FROM_HTML_FILES"] = "True"

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
            # Log failing notebook immediately to the shared error log.
            try:
                with ERROR_LOG_PATH.open("a", encoding="utf-8") as f:
                    f.write(f"{notebook_path}\n")
            except Exception:
                pass
            return False
        else:
            print(f"{GREEN}✔{RESET} Notebook {notebook_path} executed successfully.")
            write_timestamp_to_log(last_run_file)
            return True

    else:
        print(f"{BLUE}●{RESET} Notebook {notebook_path} is up to date. No execution needed.")
        return True


def main(force=False, notebook: Path = None, recursive: bool = False, n_workers: int = 1):

    if notebook is not None:
        if not notebook.exists():
            print(f"{RED}✘{RESET} {notebook} does not exist.")
            return
        if notebook.is_file():
            nb_list = [notebook]
        elif notebook.is_dir():
            if recursive:
                nb_list = notebook.rglob("*.ipynb")
            else:
                nb_list = notebook.glob("*.ipynb")
    else:
        if recursive:
            nb_list = Path(".").rglob("*.ipynb")
        else:
            nb_list = Path(".").glob("*.ipynb")

    nb_list = [nb for nb in nb_list if ".ipynb_checkpoints" not in nb.parts]

    n_workers = max(1, int(n_workers) if n_workers is not None else 1)

    failed_notebooks = []

    if n_workers == 1:
        for nb_path in nb_list:
            try:
                ok = execute_notebook(nb_path, force)
            except Exception:
                ok = False
                # Log unexpected failures (outside execute_notebook) immediately.
                try:
                    with ERROR_LOG_PATH.open("a", encoding="utf-8") as f:
                        f.write(f"{nb_path}\n")
                except Exception:
                    pass
            if not ok:
                failed_notebooks.append(nb_path)
    else:
        print(f"Executing {len(nb_list)} notebooks using {n_workers} workers.")
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            future_to_nb = {
                executor.submit(execute_notebook, nb_path, force): nb_path
                for nb_path in nb_list
            }
            for future, nb_path in future_to_nb.items():
                try:
                    ok = future.result()
                except Exception:
                    ok = False
                    # Log unexpected failures (outside execute_notebook) immediately.
                    try:
                        with ERROR_LOG_PATH.open("a", encoding="utf-8") as f:
                            f.write(f"{nb_path}\n")
                    except Exception:
                        pass
                if not ok:
                    failed_notebooks.append(nb_path)

    if failed_notebooks:
        print(f"{RED}✘{RESET} {len(failed_notebooks)} notebook(s) failed. "
              f"See {ERROR_LOG_PATH}")
    else:
        print(f"{GREEN}✔{RESET} All notebooks executed successfully.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="""
    Execute Jupyter notebooks if they have been modified since their last successful execution.
    You can pass a single notebook path, a directory, or a wildcard pattern (e.g. '*.ipynb').
    
    Examples:
        python execute_notebooks.py                       # All notebooks in current directory
        python execute_notebooks.py -r                    # All notebooks recursively from current directory
        python execute_notebooks.py -n 4 -r               # Recursively using 4 workers in parallel
        python execute_notebooks.py -r docs/user_guide    # All notebooks in docs/user_guide recursively
        python execute_notebooks.py analysis.ipynb        # Only that notebook
        python execute_notebooks.py '/home/user/*.ipynb'  # Wildcard pattern (quoted)
        python execute_notebooks.py -f                    # Force re-execution of all
        python execute_notebooks.py -fr docs/user_guide   # Combine flags: force + recursive
    
    Each successful run updates a corresponding .nbconvert.log file with a timestamp.
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
        # If we cannot reset the log, continue execution; failures will still be reported on stdout.
        pass

    if args.notebook:
        for nb in map(Path, args.notebook):
            if nb.is_file():
                main(force=args.force, notebook=nb, recursive=args.recursive, n_workers=args.n_workers)
            elif nb.is_dir():
                main(force=args.force, notebook=nb, recursive=args.recursive, n_workers=args.n_workers)
            else:
                print(f"{RED}✘{RESET} File not found or not a notebook: {nb}")
    else:
        main(force=args.force, recursive=args.recursive, n_workers=args.n_workers)
