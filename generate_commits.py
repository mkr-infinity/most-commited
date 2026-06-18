#!/usr/bin/env python3
import os, sys, subprocess, time, math

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
COUNT_FILE = os.path.join(REPO_DIR, ".commit_count")
LEDGER_FILE = os.path.join(REPO_DIR, "src", "commits.txt")

AUTHOR_NAME = "mohammadkaifraja"
AUTHOR_EMAIL = "mohammadkaifraja2@gmail.com"
os.environ.update({
    "GIT_AUTHOR_NAME": AUTHOR_NAME,
    "GIT_AUTHOR_EMAIL": AUTHOR_EMAIL,
    "GIT_COMMITTER_NAME": AUTHOR_NAME,
    "GIT_COMMITTER_EMAIL": AUTHOR_EMAIL,
})

EMOJIS = [
    "🚀", "✨", "🔥", "🌈", "🎨", "💎", "⚡", "💫", "🌟", "⭐",
    "🎯", "🎪", "🎭", "🎬", "🎤", "🎧", "🎲", "🎳", "💪", "🤖",
    "👾", "🎮", "🕹️", "💻", "🖥️", "📱", "🔧", "🛠️", "⚙️", "🔩",
    "🧰", "📦", "🎁", "🏆", "🥇", "💯", "💥", "🌊", "🌀", "🌙",
    "☀️", "🌍", "🌋", "🏔️", "🗻", "🌴", "🌲", "🌳", "🌿", "🍀",
    "🌸", "🌺", "🌻", "🌹", "🌷", "🌼", "🍃", "🍂", "🍁", "🌵",
    "🎄", "🎋", "🎍", "🎑", "🎆", "🎇", "🎉", "🎊", "🎈", "🎃",
    "🦋", "🐞", "🐛", "🦄", "🐉", "🦅", "🦁", "🐯", "🐺", "🦊",
    "🚴", "🏋️", "🤸", "🤹", "🍜", "🍕", "🥑", "🧠", "👑", "🔮",
    "📡", "🎸", "🎺", "🎻", "🥁",
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

def git(args, **kwargs):
    return subprocess.run(["git"] + args, capture_output=True, text=True, **kwargs)

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if count == 0:
        print(read_count())
        return

    commit_num = read_count()
    start_num = commit_num + 1
    end_num = commit_num + count

    parent = git(["rev-parse", "HEAD"]).stdout.strip()
    tree = git(["rev-parse", "HEAD^{tree}"]).stdout.strip()

    now_ts = int(time.time())
    total_emoji = len(EMOJIS)
    total_msgs = len(MESSAGES)

    print(f"Generating {count} commits (#{start_num} to #{end_num})...")

    for i in range(count):
        n = start_num + i
        emoji = EMOJIS[(n - 1) % total_emoji]
        msg_text = MESSAGES[(n - 1) % total_msgs]
        ts = now_ts + i
        date_str = time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime(ts))
        commit_msg = f"{emoji} commit #{n} — {msg_text} {emoji}"

        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = date_str
        env["GIT_AUTHOR_DATE"] = date_str

        r = git(["commit-tree", tree, "-p", parent], input=commit_msg, env=env)
        parent = r.stdout.strip()

        if (i + 1) % 50000 == 0:
            print(f"  ✅ {n} commits generated ({i+1}/{count})")

    git(["update-ref", "HEAD", parent])
    commit_num = end_num

    with open(COUNT_FILE, "w") as f:
        f.write(str(commit_num))

    os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
    with open(LEDGER_FILE, "w") as f:
        f.write(f"""{"═" * 59}
  MOST-COMMITED LEDGER
{"═" * 59}

  Total Commits: {commit_num}
  Last Updated:  {time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}

  Every commit is a step toward greatness.

""")

    git(["add", LEDGER_FILE, COUNT_FILE])

    final_emoji = EMOJIS[(commit_num - 1) % total_emoji]
    final_msg = MESSAGES[(commit_num - 1) % total_msgs]
    amend_msg = f"{final_emoji} commit #{commit_num} — {final_msg} {final_emoji}"
    final_ts = time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime())

    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = final_ts
    env["GIT_AUTHOR_DATE"] = final_ts
    git(["commit", "--amend", "-m", amend_msg], env=env)

    print(commit_num)

def read_count():
    try:
        with open(COUNT_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

if __name__ == "__main__":
    main()
