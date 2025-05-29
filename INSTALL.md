# 開発手順

何が開発なのやら怪しいが、いちおう記す。

## 環境整備

新しく PC を入手した後に見たい記述をここに残すべきだ。そうしよう。

Git と Python は使用可能と仮定する。

Markdown ファイル一式を HTML に変換するのに Python パッケージ [MkDocs] が必要。
プロジェクト構成ファイル `pyproject.toml` を後で用意するはずだが、それまでは手動で
Python 仮想環境を作成して MkDocs をインストールして作業すればいい。

```console
git clone git@github.com:showa-yojyo/taoup.git
cd taoup
```

ファイル `myproject.toml` がない時点では Python 仮想環境に応じて次のコマンドを使い分けろ：

* `pip install mkdocs`
* `pipenv run pip install mkdocs`
* `conda install mkdocs` or `mamba install mkdocs`
* etc.

## テスト

HTML ファイルの見栄えを肉眼で確認するには `mkdocs serve` で Web ブラウザーを開くとよい。

```console
mkdocs serve -os
```

## 成果物を GitHub Pages に送る

通常は Markdown ファイルの `main` ブランチに対する更新により、GitHub Actions のワークフローが発動して
HTML ファイルを機械的にビルド、配備される仕組みを用いる。

手動でビルドを配備する場合には下記のようにする。この手順は原稿と成果物の整合性が壊れることから咎められる。

### 自力で更新する方法

参考：<https://github.com/mkdocs/mkdocs/discussions/2599>

```console
cd taoup
mkdocs build -s
git switch gh-pages
git rm -rf .
mv site/* .
rmdir site
touch .nojekyll
git add .
git commit -m "Deploy MkDocs to GitHub Pages"
git push origin gh-pages
```

必要なブランチ `gh-pages` はすでに定義されている。

次に述べる [MkDocs] の専用コマンドを利用しない場合、ダミーファイル `.nojekyll`
を手動で作成する必要があることに注意しろ。

### `mkdocs gh-deploy` による方法

繰り返すが、このコマンド実行は咎められる。

```console
cd taoup
mkdocs gh-deploy -m "Deploy MkDocs to GitHub Pages" -s
```

[MkDocs]: <https://www.mkdocs.org/>
