<div align="center">

# 🚀 Most Committed

**Automated commit generator — build your GitHub commit history with emojis, style, and consistency.**

<br>

![Commits](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/mkr-infinity/most-commited/main/badge.json)
![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Script](https://img.shields.io/badge/script-bulk_commit_generator-7B2FF7?style=for-the-badge)

<br>

</div>

---

## 📌 About

This project generates real Git commits automatically. Each commit includes a unique number, a randomized emoji, and a clean commit message. The goal is to grow the commit count safely and consistently.

Created by **mkr-infinity** to push the limits of what's possible with automation on GitHub.

---

## ✨ Features

| | |
|---|---|
| 🔢 | Sequentially numbered commits |
| 😄 | Rotates through 100+ emojis |
| 💬 | Randomized commit messages |
| 📝 | Writes real file changes per commit |
| ✅ | Fully interactive CLI with prompts |
| 📤 | Optional auto-push to GitHub |

---

## 🚀 Getting Started

**Prerequisites:** Python 3.8+, Git, and a GitHub repository.

```bash
# Clone the repo
git clone https://github.com/mkr-infinity/most-commited.git
cd most-commited

# Run the generator
python3 bulk-commit-generator.py
```

The script guides you through every step — how many commits, whether to sign, and whether to push.

**Example:**

```bash
$ python3 bulk-commit-generator.py
Enter number of commits: 100
Push to GitHub? [y/N]: y
```

---

## ⚙️ Options

| Setting | Description | Default |
|---|---|---|
| Commit count | Number of commits to generate | Prompted |
| Sign commits | GPG-sign each commit | No |
| Push | Auto-push to remote after generation | No |
| Target folder | Folder for activity log files | `src` |

---

## 📋 Notes

- Keep batches under **5,000** on low-RAM machines.
- Commits appear on your GitHub profile if your commit email is verified.

---

## 👤 Author

**mkr-infinity** — [github.com/mkr-infinity](https://github.com/mkr-infinity)

---

<div align="center">

⭐ **Star this repository if you find it useful**

<br>
<sub>Copyright © 2026 Mohammad Kaif Raja</sub>

</div>
