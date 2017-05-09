set -e
pip install doctr
cd docs
make html
cd ..
doctr deploy .