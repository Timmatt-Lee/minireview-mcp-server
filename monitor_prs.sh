#!/bin/bash

while true; do
  open_prs=$(gh pr list --state open --json number -q '.[].number')

  if [ -z "$open_prs" ]; then
    echo "No open pull requests to monitor. Exiting."
    break
  fi

  merged_prs=()
  for pr_number in $open_prs; do
    status=$(gh pr view "$pr_number" --json state -q .state)
    if [ "$status" == "MERGED" ]; then
      echo "PR #$pr_number has been merged."
      merged_prs+=("$pr_number")
    fi
  done

  if [ ${#merged_prs[@]} -gt 0 ]; then
    echo "One or more PRs have been merged. Switching to main and pulling."
    git checkout main
    git pull
    echo "Switched to main and pulled the latest changes."

    for pr_number in "${merged_prs[@]}"; do
      branch_name=$(gh pr view "$pr_number" --json headRefName -q .headRefName)
      if [ -n "$branch_name" ]; then
        echo "Deleting local branch for PR #$pr_number: $branch_name"
        git branch -d "$branch_name"
      fi
    done
  fi

  open_prs_after_pull=$(gh pr list --state open --json number -q '.[].number')
  if [ -z "$open_prs_after_pull" ]; then
    echo "All pull requests have been merged. Exiting."
    break
  fi

  echo "No PRs merged yet. Still monitoring open PRs: $open_prs. Checking again in 10 seconds."
  sleep 10
done
