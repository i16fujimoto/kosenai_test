FROM python:3.8
ENV PYTHONUNBUFFERED 1

# パッケージリストを更新し，インストール済みのパッケージを更新
RUN apt update && apt upgrade -y

RUN mkdir /src
# コンテナにアクセスした際のデフォルトディレクトリ
WORKDIR /src

# Dockerfileより上の階層は見れない（ex. ../）
COPY ./requirements.txt /src/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# poetryの定義ファイルをコピー
COPY ./src/pyproject.toml* /src/
COPY ./src/poetry.lock* /src/

# pytest.iniをコピー
COPY ./src/pytest.ini /src

# # poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.create false && if [ -f pyproject.toml ]; then poetry install; else poetry init; fi
