<div align="center">

<a href="https://github.com/mkr-infinity/most-commited">

<img src="https://img.shields.io/badge/-Most%20Committed-black?style=for-the-badge&logo=github&logoColor=white" alt="Most Committed">

</a>

<br>
<br>

<h1>Most Committed</h1>

<p>A testing ground for Git commits. Push as many as you want, break things, try stuff — this repo exists for that.</p>

<br>

![Commits](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/mkr-infinity/most-commited/main/badge.json)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Script](https://img.shields.io/badge/Script-bulk--commit--generator-7B2FF7?style=for-the-badge&logo=terminal&logoColor=white)

<br>

</div>

---

<br>

<div align="center">

## 🎯 What is this?

</div>

<br>

This repo is for **testing Git** — commit patterns, bulk pushes, workflow automation, whatever you want to try.

It comes with a commit generator script that creates numbered commits with emojis and messages. Use it, modify it, or ignore it — up to you.

<br>

---

<br>

<div align="center">

## ✨ What's inside

</div>

<table>
<tr>
<td>

🔢 **Numbered commits**

Every commit gets a unique number.

</td>
<td>

😄 **100+ emojis**

Commits rotate through different emojis.

</td>
<td>

💬 **Clean messages**

Each commit has a randomized message.

</td>
</tr>
<tr>
<td>

📝 **Real changes**

Writes actual file changes to the repo.

</td>
<td>

✅ **Interactive CLI**

Guided prompts — just answer and go.

</td>
<td>

📤 **Auto push**

Optionally push to GitHub after.

</td>
</tr>
</table>

<br>

---

<br>

<div align="center">

## 🚀 How to use

</div>

<br>

### Option A — Run locally

```bash
git clone https://github.com/mkr-infinity/most-commited.git
cd most-commited
python3 bulk-commit-generator.py
```

Follow the prompts — enter commit count, choose to push, done.

<br>

### Option B — GitHub Actions

<br>

**Step 1 — Set up secrets (one time)**

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Value |
|---|---|
| `GIT_USER_NAME` | Your GitHub username |
| `GIT_USER_EMAIL` | Your verified GitHub email |

<br>

**Step 2 — Run the workflow**

1. Go to **Actions** → **Generate Commits**
2. Click **Run workflow**
3. Enter commit count (e.g. `1000`)
4. Toggle push (`true` / `false`)
5. Click **Run**

The script runs on GitHub's servers using your secrets for author identity.

<br>

---

<br>

<div align="center">

## ⚙️ CLI usage

</div>

<br>

```bash
# Non-interactive — no prompts
python3 bulk-commit-generator.py --count 1000 --push

# With signed commits
python3 bulk-commit-generator.py --count 500 --signed --push

# Just generate, no push
python3 bulk-commit-generator.py --count 100
```

| Flag | Description |
|---|---|
| `--count N` | Number of commits to generate |
| `--signed` | GPG-sign each commit |
| `--push` | Push to remote after generation |

<br>

---

<br>

<div align="center">

## 💡 Tips

</div>

<br>

| | |
|---|---|
| 🖥️ | Low RAM? Keep batches under **5,000** |
| 📧 | Commits count if your commit email is verified on GitHub |
| 🔁 | Run the script multiple times to grow your count |

<br>

---

<br>

<div align="center">

## 👑 Made by

[**mkr-infinity**](https://github.com/mkr-infinity)

*Testing Git, one commit at a time.*

<br>

⭐ **Star this repo if you like the grind** ⭐

<br>

<sub>Copyright © 2026 Mohammad Kaif Raja</sub>

</div>
