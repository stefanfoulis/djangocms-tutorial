#!/bin/bash
git checkout start
text="$(cat README.md)"

for branch in step-1 step-2 step-3 step-4 step-5 step-6
do
	git checkout $branch
	text="$text\n\n$(cat README.md)"
done

git checkout master

echo -e "$text" > README.md
