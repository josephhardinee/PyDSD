set -e
pip install doctr
cd "$TRAVIS_BUILD_DIR"
cd docs
make html
cd ..
doctr deploy .
