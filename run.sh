#!/bin/sh

# Checks for updates via github
update() {
  UPSTREAM=${1:-'@{u}'}
  LOCAL=$(git rev-parse @)
  REMOTE=$(git rev-parse "$UPSTREAM")
  BASE=$(git merge-base @ "$UPSTREAM")

  if [ $LOCAL = $REMOTE ]; then
    echo "Bot is up-to-date"
  elif [ $LOCAL = $BASE ]; then
    echo "Updating bot..."
    git fetch
  fi
}

# Runs bot
run() {
  pipenv run python jb-bot.py
}

update
run
