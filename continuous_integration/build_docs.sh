#!/bin/bash
# Adapted from the ci/build_docs.sh file from the pandas project
# https://github.com/pydata/pandas
set -e

cd "$TRAVIS_BUILD_DIR"

echo "Building Docs"
conda install -q sphinx PIL

cd "$TRAVIS_BUILD_DIR"/docs
make html
mv "$TRAVIS_BUILD_DIR"/docs/build/html /tmp


if [ "$TRAVIS_PULL_REQUEST" == "false" ] && [ $TRAVIS_SECURE_ENV_VARS == 'true' ]; then

    cd "$TRAVIS_BUILD_DIR"
    rm -rf *
    git init .
    git checkout gh-pages

    mv /tmp/html/* ./

    git config --global user.email "pydisdrometer-docs-bot@example.com"
    git config --global user.name "pydisdrometer-docs-bot"

    touch .nojekyll
    git add --all .
    git commit -m "Version" --allow-empty -q
    git remote add origin https://$GH_TOKEN@github.com/https://github.com/josephhardinee/PyDisdrometer.git &> /dev/null
    git push origin gh-pages -fq &> /dev/null
fi

exit 0
