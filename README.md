# Most Committed

Goal: become one of the most committed repos on GitHub.

## How It Works

- `generate_commits.py` creates empty commits with emoji messages.
- GitHub Actions runs it automatically every 6 hours.
- Commits use `mohammadkaifraja2@gmail.com`, so they count if that email is verified on GitHub.

## Run

Go to **Actions** → **Generate Commits** → **Run workflow**.

Automated batch size: `50000` commits per run.

Manual runs are capped at `50000` commits.

## Note

Do not push millions of commits at once. Use batches to avoid GitHub account or repository problems.
