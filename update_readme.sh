#!/bin/bash
git checkout gh-pages

for branch in start step-1 step-2 step-3 step-4 step-5 step-6
do
	git checkout $branch
	text="$text\n\n$(cat README.md)"
done

git checkout gh-pages

echo -e "$text" > publish_me.md
echo -e "$text" | pandoc -f markdown -t html -o publish_me.html

#git checkout gh-pages
#git add index.html
#git commit -m "updated README"
#git push
