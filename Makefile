all:
	fd . | PYTHONDONTWRITEBYTECODE=1 entr -cc pytest
