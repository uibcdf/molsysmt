import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import argparse


def write_timestamp_to_log(log_path: Path):
    timestamp = datetime.now(timezone.utc).timestamp()
    log_path.write_text(f"{timestamp:.6f}")
    print(f"🕒 Timestamp written to {log_path}: {timestamp:.6f}")
    return timestamp

def read_timestamp_from_log(log_path: Path) -> float:
    try:
        return float(log_path.read_text().strip())
    except Exception:
        return 0.0

def execute_notebook(notebook_path: Path, force: bool = False) -> bool:

    last_run_file = notebook_path.with_suffix('.nbconvert.last_run')
    stdout_log_file = notebook_path.with_suffix('.nbconvert.stdout.log')
    stderr_log_file = notebook_path.with_suffix('.nbconvert.stderr.log')

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
        env["MOLSYSMT_DOCS_BUILDING"] = "true"

        result = subprocess.run(
            ["jupyter", "nbconvert", "--execute", "--inplace", str(notebook_path)],
            capture_output=True,
            text=True,
            env=env
        )

        stdout_log_file.write_text(result.stdout)
        stderr_log_file.write_text(result.stderr)

        if result.returncode != 0:
            print(f"Error executing {notebook_path}: check {stderr_log_file}")
            if last_run_file.exists():
                last_run_file.unlink()
            return False
        else:
            print(f"Notebook {notebook_path} executed successfully.")
            write_timestamp_to_log(last_run_file)
            return True

    else:
        print(f"Notebook {notebook_path} is up to date. No execution needed.")
        return True

def main(force=False, notebook: Path = None):

    if not notebook.exists():
        print(f"{notebook} does not exist.")
        return

    if notebook is not None:
        if notebook.is_file():
            nb_list = [notebook]
        elif notebook.is_dir():
            nb_list = notebook.glob("*.ipynb")
    else:
        nb_list = Path(".").glob("*.ipynb")

    for nb_path in nb_list:
        status_execution = execute_notebook(nb_path, force)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Execute .ipynb files if updated.")
    parser.add_argument("notebook", nargs="?", default=None,
                        help="Specific notebook to execute (optional).")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force execution of notebooks regardless of timestamps.")
    args = parser.parse_args()

    if args.notebook:
        nb_path = Path(args.notebook)
        main(force=args.force, notebook=nb_path)
    else:
        main(force=args.force)

