# overleaf-to-git

## Required setup

1. Install Python 3.10.
1. Run `./setup.sh` script.
1. Activate created venv with `. .venv/bin/activate`.
1. Login with `ols login` (requires GUI support!)
    - This will generate `.olauth` file that you could generate
      on a different (desktop) machine and copy it over to a server.
1. Clone target repository to `repo` subdirectory.
    - The script expects two branches: `main` and `labels`
    - The script expects an `origin` remote to be set
    - Author name is taken from version information
    - Author email needs to be set up on the machine to a proper value manually
1. `OLS_PROJECT_NAME` env var should be set to the name of the project on Overleaf.

## Usage

`./overleaf_git_sync.py`
