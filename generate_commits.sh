#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
COUNT_FILE="$REPO_DIR/.commit_count"
LEDGER_FILE="$REPO_DIR/src/commits.txt"

export GIT_AUTHOR_NAME="most-commited-bot"
export GIT_AUTHOR_EMAIL="bot@most-commited.dev"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

## ─── 105 unique emojis ────────────────────────────────────
EMOJIS=(
  "🚀" "✨" "🔥" "🌈" "🎨" "💎" "⚡" "💫" "🌟" "⭐"
  "🎯" "🎪" "🎭" "🎬" "🎤" "🎧" "🎲" "🎳" "💪" "🤖"
  "👾" "🎮" "🕹️" "💻" "🖥️" "📱" "🔧" "🛠️" "⚙️" "🔩"
  "🧰" "📦" "🎁" "🏆" "🥇" "💯" "💥" "🌊" "🌀" "🌙"
  "☀️" "🌍" "🌋" "🏔️" "🗻" "🌴" "🌲" "🌳" "🌿" "🍀"
  "🌸" "🌺" "🌻" "🌹" "🌷" "🌼" "🍃" "🍂" "🍁" "🌵"
  "🎄" "🎋" "🎍" "🎑" "🎆" "🎇" "🎉" "🎊" "🎈" "🎃"
  "🦋" "🐞" "🐛" "🦄" "🐉" "🦅" "🦁" "🐯" "🐺" "🦊"
  "🚴" "🏋️" "🤸" "🤹" "🍜" "🍕" "🥑" "🧠" "👑" "🔮"
  "📡" "🎸" "🎺" "🎻" "🥁"
)

TOTAL_EMOJIS=${#EMOJIS[@]}

## ─── Beautiful commit messages ──────────────────────────
MESSAGES=(
  "another step forward!"
  "on the grind!"
  "never stopping!"
  "pushing limits!"
  "making history!"
  "relentless!"
  "keep going!"
  "building legacy!"
  "one more!"
  "count it!"
  "another brick!"
  "onward!"
  "progress!"
  "numbers go up!"
  "no days off!"
  "consistency!"
  "dedication!"
  "passion!"
  "excellence!"
  "greatness!"
  "hustle!"
  "grind mode!"
  "can't stop!"
  "won't stop!"
  "unstoppable!"
  "moving forward!"
  "getting stronger!"
  "never give up!"
  "dream big!"
  "legendary!"
)

TOTAL_MSGS=${#MESSAGES[@]}

## ─── Parse input ────────────────────────────────────────
COMMITS_TO_MAKE="${1:-1}"

if [ "$COMMITS_TO_MAKE" -eq 0 ]; then
  echo "$(cat "$COUNT_FILE" 2>/dev/null || echo 0)"
  exit 0
fi

## ─── Resume from last count ─────────────────────────────
if [ -f "$COUNT_FILE" ]; then
  COMMIT_NUM=$(cat "$COUNT_FILE")
else
  COMMIT_NUM=0
fi

## ─── Current tree (all lightweight commits share this) ──
BASE_TREE=$(git rev-parse HEAD^{tree} 2>/dev/null || echo "4b825dc642cb6eb9a060e54bf899d153036d1a9b")

START_NUM=$((COMMIT_NUM + 1))
END_NUM=$((COMMIT_NUM + COMMITS_TO_MAKE))
NOW=$(date +%s)

echo "Generating $COMMITS_TO_MAKE commits (commits $START_NUM to $END_NUM)..."

## ─── Generate lightweight commits via commit-tree ───────
for ((N = START_NUM; N <= END_NUM; N++)); do
  EMOJI="${EMOJIS[$(( (N - 1) % TOTAL_EMOJIS ))]}"
  MSG_TEXT="${MESSAGES[$(( (N - 1) % TOTAL_MSGS ))]}"

  TS=$((NOW + N - START_NUM))
  DATE_LINE="$(date -u '+%Y-%m-%d %H:%M:%S +0000' -d "@$TS")"
  COMMIT_MSG="$EMOJI commit #$N — $MSG_TEXT $EMOJI"

  NEW_COMMIT=$(echo "$COMMIT_MSG" | GIT_COMMITTER_DATE="$DATE_LINE" GIT_AUTHOR_DATE="$DATE_LINE" \
    git commit-tree "$BASE_TREE" -p HEAD)
  git update-ref HEAD "$NEW_COMMIT"

  if [ $((N % 25000)) -eq 0 ]; then
    echo "  ✅ $N commits generated so far..."
  fi
done

COMMIT_NUM=$END_NUM
echo "$COMMIT_NUM" > "$COUNT_FILE"

## ─── Final commit: write the ledger ─────────────────────
mkdir -p "$REPO_DIR/src"
{
  echo "═══════════════════════════════════════════════════════════"
  echo "  MOST-COMMITED LEDGER"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "  Total Commits: $COMMIT_NUM"
  echo "  Last Updated:  $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo ""
  echo "  Every commit is a step toward greatness."
  echo ""
} > "$LEDGER_FILE"

git add "$LEDGER_FILE" "$COUNT_FILE"

FINAL_TS="$(date -u '+%Y-%m-%d %H:%M:%S +0000')"
FINAL_EMOJI="${EMOJIS[$(( (COMMIT_NUM - 1) % TOTAL_EMOJIS ))]}"
FINAL_MSG="${MESSAGES[$(( (COMMIT_NUM - 1) % TOTAL_MSGS ))]}"
AMEND_MSG="$FINAL_EMOJI commit #$COMMIT_NUM — $FINAL_MSG $FINAL_EMOJI"

GIT_COMMITTER_DATE="$FINAL_TS" GIT_AUTHOR_DATE="$FINAL_TS" \
  git commit --amend -m "$AMEND_MSG"

echo "$COMMIT_NUM"
