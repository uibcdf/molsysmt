#/bin/bash

if git diff-index --quiet HEAD --; then

    echo "Updating gh-pages branch"

    cd ..
    git checkout gh-pages
    git rm -rf *
    git checkout master docs/*
    cd docs
    make html
    mv -fv _build/html/* ./../.
    make clean
    rm -rf _build
    cd ..
    git rm -rf docs
    touch .nojekyll
    git add --all
    git commit -a -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
    git push origin gh-pages
    git checkout master
    cd docs

else

    echo "Changes in master branch need to be committed and pushed before updating gh-pages"

fi

