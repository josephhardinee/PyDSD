set -e
pip install doctr
doctr deploy
cd docs
make html
cd ..
doctr deploy .