<div align="center">

<a href="https://github.com/mkr-infinity/most-commited">

<img src="https://img.shields.io/badge/-Most%20Committed-black?style=for-the-badge&logo=github&logoColor=white" alt="Most Committed">

</a>

<br>
<br>

### **Build your GitHub commit history.**

<br>

![Commits](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/mkr-infinity/most-commited/main/badge.json)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Script](https://img.shields.io/badge/Script-bulk--commit--generator-7B2FF7?style=for-the-badge&logo=terminal&logoColor=white)

<br>

</div>

---

<br>

<div align="center">

## 💡 What is this?

A Python script that creates **real Git commits** automatically.

Each commit has a **number**, a **different emoji**, and a **beautiful message**.

**Why?** To build one of the most committed repositories on GitHub.

<br>

</div>

---

<br>

## ✨ What you get

<table>
<tr>
<td>

🔢 **Numbered commits**

Every commit gets a unique incrementing number.

</td>
<td>

😄 **100+ emojis**

Commits rotate through 100+ different emojis.

</td>
<td>

💬 **Clean messages**

Each commit has a beautiful randomized message.

</td>
</tr>
<tr>
<td>

📝 **Real changes**

Writes actual file changes to your repository.

</td>
<td>

✅ **Interactive CLI**

A guided setup — just answer the prompts.

</td>
<td>

📤 **Auto push**

Optionally push to GitHub after generation.

</td>
</tr>
</table>

<br>

---

<br>

## 🚀 How to use

<br>

### Option A — Run locally

```bash
git clone https://github.com/mkr-infinity/most-commited.git
cd most-commited
python3 bulk-commit-generator.py
```

Follow the prompts — enter commit count, choose to push, done.

### Option B — GitHub Actions

1. Go to **Actions** → **Generate Commits**
2. Click **Run workflow**
3. Enter commit count (e.g. `1000`)
4. Click **Run**

The script runs on GitHub's servers and pushes automatically.

<br>

---

<br>

## ⚙️ CLI usage (advanced)

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

## ⚠️ Tips

| | |
|---|---|
| 🖥️ | Low RAM? Keep batches under **5,000** |
| 📧 | Commits count if your commit email is verified on GitHub |
| 🔁 | Run the script multiple times to grow your count |

<br>

---

<br>

## 👑 Made by

<div align="center">

[**mkr-infinity**](https://github.com/mkr-infinity)

*Building the most committed repository on GitHub.*

<br>

⭐ **Star this repo if you like the grind** ⭐

</div>

<br>

---

<br>

<div align="center">
<sub>Copyright © 2026 Mohammad Kaif Raja</sub>
</div>
