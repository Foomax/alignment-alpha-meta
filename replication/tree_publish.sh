#!/usr/bin/env bash
# Watches tree.log; after each finished node, publishes that experiment to its Foomax fork
# (template README; refined later at judgement time by re-running publish.sh with README.human.md /
# README.llm.md present). Also commits the meta repo's replication/ folder after each node.
set -uo pipefail
REP="$(cd "$(dirname "$0")" && pwd)"; LOG="$REP/tree.log"; PLOG="$REP/tree_publish.log"
declare -A done
publish_slug() {
  local slug="$1"
  echo "== $(date -Is) publish $slug" >> "$PLOG"
  bash "$REP/publish.sh" "$slug" "replication run finished: $slug" >> "$PLOG" 2>&1 || echo "   publish FAILED for $slug" >> "$PLOG"
  ( cd "$REP/.." && git add replication >/dev/null 2>&1 && git commit -q -m "replication: $slug finished" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" >/dev/null 2>&1 && git push -q origin HEAD >/dev/null 2>&1 ) || true
}
tail -n +1 -F "$LOG" | while read -r line; do
  case "$line" in
    *"NODE 01-cross-model-geometry EXIT"*) slug="cross-model-activation-generalizability-isn-t-st--jaehoonlee0829" ;;
    *"NODE "*" EXIT "*) slug=$(echo "$line" | sed -E 's/.*NODE [0-9]+-([^ ]+) EXIT.*/\1/') ;;
    *"TREE DONE"*) echo "== $(date -Is) tree done" >> "$PLOG"; continue ;;
    *) continue ;;
  esac
  [ -n "${done[$slug]:-}" ] && continue
  done[$slug]=1
  publish_slug "$slug"
done
