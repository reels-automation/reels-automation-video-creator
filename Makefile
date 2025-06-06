install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

python-run:
	cp .env.dev .env
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && python main.py | pygmentize -g'

python-run-prod:
	cp .env.production .env
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && python main.py | pygmentize -g'
