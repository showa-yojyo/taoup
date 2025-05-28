# 開発手順

何が開発なのやら怪しいが、いちおう記す。

## 環境整備

Markdown ファイル一式を HTML に変換するのに Python パッケージ [MkDocs] が必要。

プロジェクト構成ファイル `pyproject.toml` を後で用意するはずだが、それまでは手動で
Python 仮想環境を作成して MkDocs をインストールして作業すればいい。

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

[MkDocs] のコマンドを利用する方法と、GitHub Actions を利用する方法がある。どちらも準備中。

[MkDocs]: <https://www.mkdocs.org/>
