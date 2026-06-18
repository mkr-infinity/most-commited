#!/usr/bin/env python3
"""Generate commits with emojis and beautiful messages - optimized version."""
import os, sys, subprocess, time

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
COUNT_FILE = os.path.join(REPO_DIR, ".commit_count")
LEDGER_FILE = os.path.join(REPO_DIR, "src", "commits.txt")

NAME = "mohammadkaifraja"
EMAIL = "mohammadkaifraja2@gmail.com"

EMOJIS = [
    "🚀", "✨", "🔥", "🌈", "🎨", "💎", "⚡", "💫", "🌟", "⭐",
    "🎯", "🎪", "🎭", "🎬", "🎤", "🎧", "🎲", "🎳", "💪", "🤖",
    "👾", "🎮", "🕹️", "💻", "🖥️", "📱", "🔧", "🛠️", "⚙️", "🔩",
    "🧰", "📦", "🎁", "🏆", "🥇", "💯", "💥", "🌊", "🌀", "🌈",
    "🌙", "☀️", "🌍", "🌋", "🏔️", "🗻", "🌴", "🌲", "🌳", "🌿",
    "🍀", "🌸", "🌺", "🌻", "🌹", "🌷", "🌼", "🍃", "🍂", "🍁",
    "🌵", "🎄", "🎋", "🎍", "🎑", "🎆", "🎇", "🎉", "🎊", "🎈",
    "🎃", "🦋", "🐞", "🐛", "🦄", "🐉", "🦅", "🦁", "🐯", "🐺",
    "🦊", "🚴", "🏋️", "🤸", "🤹", "🍜", "🍕", "🥑", "🧠", "👑",
    "🔮", "📡", "🎸", "🎺", "🎻", "🥁",
]

MESSAGES = [
    "another step forward!", "on the grind!", "never stopping!",
    "pushing limits!", "making history!", "relentless!", "keep going!",
    "building legacy!", "one more!", "count it!", "another brick!",
    "onward!", "progress!", "numbers go up!", "no days off!",
    "consistency!", "dedication!", "passion!", "excellence!",
    "greatness!", "hustle!", "grind mode!", "can't stop!", "won't stop!",
    "unstoppable!", "moving forward!", "getting stronger!",
    "never give up!", "dream big!", "legendary!",
]

def read_count():
    try:
        with open(COUNT_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def log(msg):
    print(msg, file=sys.stderr, flush=True)

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if count == 0:
        print(read_count())
        return

    commit_num = read_count()
    start_num = commit_num + 1
    end_num = commit_num + count
    now_ts = int(time.time())
    total_emoji = len(EMOJIS)
    total_msgs = len(MESSAGES)

    # Get current HEAD and tree
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], capture_output=True, text=True
    ).stdout.strip()

    log(f"Generating {count} commits (#{start_num} to #{end_num})...")

    parent = head
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = NAME
    env["GIT_AUTHOR_EMAIL"] = EMAIL
    env["GIT_COMMITTER_NAME"] = NAME
    env["GIT_COMMITTER_EMAIL"] = EMAIL

    for i in range(count):
        n = start_num + i
        emoji = EMOJIS[(n - 1) % total_emoji]
        msg_text = MESSAGES[(n - 1) % total_msgs]
        ts = now_ts + i
        date_str = time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime(ts))
        commit_msg = f"{emoji} commit #{n} — {msg_text} {emoji}"

        env["GIT_COMMITTER_DATE"] = date_str
        env["GIT_AUTHOR_DATE"] = date_str

        r = subprocess.run(
            ["git", "commit-tree", tree, "-p", parent],
            input=commit_msg, capture_output=True, text=True, env=env
        )
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip() or "git commit-tree failed")
        parent = r.stdout.strip()

        if (i + 1) % 50000 == 0:
            log(f"  ✅ {n} commits generated ({i+1}/{count})")

    subprocess.run(["git", "update-ref", "HEAD", parent], check=True)
    commit_num = end_num

    # Write count file
    with open(COUNT_FILE, "w") as f:
        f.write(str(commit_num))

    # Write ledger
    os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
    with open(LEDGER_FILE, "w") as f:
        f.write(f"""{"=" * 59}
  MOST-COMMITED LEDGER
{"=" * 59}

  Total Commits: {commit_num}
  Last Updated:  {time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}

  Every commit is a step toward greatness.

""")

    # Create final real commit with the ledger
    subprocess.run(["git", "add", LEDGER_FILE, COUNT_FILE], check=True)
    final_emoji = EMOJIS[(commit_num - 1) % total_emoji]
    final_msg = MESSAGES[(commit_num - 1) % total_msgs]
    final_ts = time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime())
    amend_msg = f"{final_emoji} commit #{commit_num} — {final_msg} {final_emoji}"

    env["GIT_COMMITTER_DATE"] = final_ts
    env["GIT_AUTHOR_DATE"] = final_ts
    env["GIT_AUTHOR_NAME"] = NAME
    env["GIT_AUTHOR_EMAIL"] = EMAIL
    env["GIT_COMMITTER_NAME"] = NAME
    env["GIT_COMMITTER_EMAIL"] = EMAIL
    subprocess.run(
        ["git", "commit", "--amend", "-m", amend_msg],
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    # ONLY output the number to stdout (everything else to stderr)
    print(commit_num)

if __name__ == "__main__":
    main()
