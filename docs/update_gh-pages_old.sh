#/bin/bash

if git diff-index --quiet HEAD --; then

    echo "Updating gh-pages branch"

    bash build_local_version.sh
    git add _build/html

    cd ..
    git checkout gh-pages
    rm -rf *
    git checkout master docs/_build/html/*
    mv -fv docs/_build/html/* .
    rm -rf docs
    touch .nojekyll
    git add --all
    git commit -a -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
    git push origin gh-pages
    git checkout master

    cd docs
    bash remove_local_version.sh

else

    echo "Changes in master branch need to be committed and pushed before updating gh-pages"

fi

