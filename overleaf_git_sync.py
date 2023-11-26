#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile
import time


REPO_DIR = os.getenv("REPO_DIR", "repo")


def main() -> int:
    project_name = os.environ["OLS_PROJECT_NAME"]

    subprocess.check_call(("git", "checkout", "main"), cwd=REPO_DIR)
    try:
        version = subprocess.check_output(
            ("git", "describe", "--tags", "--exact-match"),
            cwd=REPO_DIR,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        version = "0"

    subprocess.check_call(
        ("ols", "versions", "-v", "--name", project_name, "--after", version)
    )

    with open(".olversions", "r", encoding="utf-8") as fp:
        versions = json.load(fp)

    for v in reversed(versions):
        with tempfile.TemporaryDirectory() as tmpdir:
            version_number = v["toV"]
            author = v["meta"]["users"][0]
            author_name = f"{author['first_name']} {author['last_name']}"
            env = {**os.environ, "GIT_AUTHOR_NAME": author_name}
            subprocess.check_call(
                (
                    "ols",
                    "--remote-only",
                    "--path",
                    tmpdir,
                    "--name",
                    project_name,
                    "--project-version",
                    str(version_number),
                )
            )
            subprocess.check_call(("git", "checkout", "main"), cwd=REPO_DIR)
            subprocess.check_call(
                ("git", "rm", "--ignore-unmatch", "-r", "."), cwd=REPO_DIR
            )
            subprocess.check_call(("cp", "-r", f"{tmpdir}/.", REPO_DIR))
            subprocess.check_call(("git", "add", "."), cwd=REPO_DIR)
            subprocess.check_call(
                ("git", "commit", "--allow-empty", "-m", f"Version {version_number}"),
                cwd=REPO_DIR,
                env=env,
            )
            subprocess.check_call(("git", "tag", str(version_number)), cwd=REPO_DIR)
            if v["labels"]:
                label = v["labels"][0]
                subprocess.check_call(("git", "checkout", "labels"), cwd=REPO_DIR)
                subprocess.check_call(
                    ("git", "rm", "--ignore-unmatch", "-r", "."), cwd=REPO_DIR
                )
                subprocess.check_call(("cp", "-r", f"{tmpdir}/.", REPO_DIR))
                subprocess.check_call(("git", "add", "."), cwd=REPO_DIR)
                subprocess.check_call(
                    ("git", "commit", "--allow-empty", "-m", label["comment"]),
                    cwd=REPO_DIR,
                    env=env,
                )

        time.sleep(1)

    subprocess.check_call(("git", "checkout", "main"), cwd=REPO_DIR)
    subprocess.check_call(("git", "push", "origin", "main"), cwd=REPO_DIR)
    subprocess.check_call(("git", "push", "origin", "labels"), cwd=REPO_DIR)
    subprocess.check_call(("git", "push", "--tags"), cwd=REPO_DIR)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
