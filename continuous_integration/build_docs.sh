cd "$TRAVIS_BUILD_DIR"
cd docs
make html
doctr deploy .
