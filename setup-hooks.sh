#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

ln -s ../../.hooks/pre-commit .git/hooks/pre-commit

echo "Completed symlinking git hooks"
