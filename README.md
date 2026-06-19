<div align="center">

# 🚀 Most Committed

**Automated commit generator — build your GitHub commit history with emojis, style, and consistency.**

<p>
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mkr-infinity/most-commited/main/badge.json" alt="commits">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/github/license/mkr-infinity/most-commited?style=flat-square" alt="license">
</p>

</div>

---

## 📌 About

This project generates real Git commits automatically. Each commit includes a unique number, a randomized emoji, and a clean commit message. The goal is simple — grow the commit count safely and consistently.

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

### Prerequisites

- Python 3.8 or higher
- Git installed and configured
- A GitHub repository (this one)

### Installation

```bash
git clone https://github.com/mkr-infinity/most-commited.git
cd most-commited
```

### Usage

```bash
python3 bulk-commit-generator.py
```

The script will guide you through an interactive setup:
1. Enter the number of commits to generate
2. Choose whether to sign commits (optional)
3. Confirm and watch the commits roll in
4. Optinally push to GitHub

### Example

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
| Sign commits | GPG-sign each commit (requires GPG setup) | No |
| Push | Automatically push to remote after generation | No |
| Target folder | Folder for activity log files | `src` |

---

## 📋 Notes

- Keep batch sizes under **5,000** on low-RAM machines.
- Commits appear on your GitHub profile if your commit email is verified.
- The repository uses `git commit --allow-empty` style commits with real file tracking.

---

## 👤 Author

**mkr-infinity** — [GitHub Profile](https://github.com/mkr-infinity)

---

<div align="center">

⭐ **Star this repository if you find it useful**

<br>

<sub>Copyright © 2026 Mohammad Kaif Raja. All rights reserved.</sub>

</div>
