#/bin/bash

if git diff-index --quiet HEAD --; then

    echo "Updating pages"

    bash remove_local_version.sh

    make html

    git add build

    git commit -a -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
    git push

else

    echo "Changes in master branch need to be committed and pushed before updating gh-pages"

fi

