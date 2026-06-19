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

<br>

</div>

---

<br>

<div align="center">

## 🎯 What is this?

</div>

<br>

A repo for **testing Git** — commit patterns, bulk pushes, workflow automation, whatever you want to try.

Comes with two commit generators — one Python script, one pure YAML workflow. Use whichever you like.

<br>

---

<br>

<div align="center">

## ✨ Workflows

</div>

<br>

### Generate Commits

Runs the Python script. Creates numbered commits with emojis and messages. No push.

**Setup — secrets (one time)**

Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Value |
|---|---|
| `GIT_USER_NAME` | Your GitHub username |
| `GIT_USER_EMAIL` | Your verified GitHub email |

Then go to **Actions** → **Generate Commits** → **Run workflow**.

<br>

### Empty Commits

Pure YAML — no Python needed. Creates empty commits with numbers, emojis, and messages directly in the workflow.

Go to **Actions** → **Empty Commits** → enter count → **Run**.

<br>

---

<br>

<div align="center">

## 💡 Tips

</div>

<br>

| | |
|---|---|
| 📧 | Commits count if your commit email is verified on GitHub |
| 🚫 | These workflows do not push — commits stay local to the runner |
| 🔁 | Run multiple times to grow your count |

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
