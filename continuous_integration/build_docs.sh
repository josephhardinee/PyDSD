set -e
pip install doctr pillow
cd docs
make clean
make html
cd ..
doctr deploy .
