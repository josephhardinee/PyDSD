set -e
pip install doctr pillow
cd docs
make html
cd ..
doctr deploy .