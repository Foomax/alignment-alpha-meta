#!/usr/bin/env bash
# Mirror the whole meta-analysis repo (minus rebuildable venvs) + the 3090 prompts to the external drive.
# Runs once, or loops every 10 min with --loop. NTFS target: symlinks (venv python) are not copied; everything else is.
DEST=/media/user/466CD2B96CD2A34B/home/alignment-replication-3090-2026-08
sync_once() {
  rsync -a --delete --no-links --exclude '.venv/' --exclude 'experiments/*/.venv/' --exclude '__pycache__/' --exclude 'env/' \
        "$HOME/alignment-literature-meta-analysis/" "$DEST/alignment-literature-meta-analysis/" 2>>"$DEST/mirror.err"
  rsync -a --delete "$HOME/prompts/" "$DEST/prompts/" 2>>"$DEST/mirror.err"
  rsync -a "$HOME/.claude/projects/-home-user-prompts/memory/" "$DEST/claude-memory/" 2>>"$DEST/mirror.err"
  date -Is > "$DEST/last-mirror.txt"
}
if [ "${1:-}" = "--loop" ]; then while [ ! -f "$DEST/mirror.stop" ]; do sync_once; sleep 600; done; else sync_once; fi
