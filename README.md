# The Art of Unix Programming 読書ノート

公に見られる場所に置く文書ではあるが、個人的な用途で書いたものなのでこの `README` も日本語で書く。

## プロジェクト概要

このリポジトリーは [*The Art of Unix Programming*][TAOUP] (2003, Eric S. Raymond)
（以下 [TAOUP] と略す）についての個人的な読書ノートだ。

その本曰く、

> In your source code, include the standard metainformation files described in
> the Chapter 19 section on open-source release practices, such as `README`.
> Even if your code is going to be proprietary, these are Unix conventions and
> future maintainers coming from a Unix background will come up to speed faster
> if the conventions are followed. (Chapter 18)
<!-- および -->
> `README` files should be short and easy to read. Make yours an introduction,
> not an epic. (Chapter 19)

とのことなので、このファイルを記す。

## プロジェクトサイト

GitHub に置いてある次のページが [TAOUP] 読書ノートのリポジトリーを含むプロジェクト拠点の URL だ：

* TAOUP 読書ノート
  * [showa-yojyo/taoup](https://github.com/showa-yojyo/taoup/): 本プロジェクト。
  * [GitHub Pages](https://showa-yojyo.github.io/taoup/): 閲覧用ファイル。
* [読書ノート](https://github.com/showa-yojyo/notebook/): 上位プロジェクト。

## ビルド環境とありそうな問題

読書ノートは Markdown 形式で記しているので、汎用テキストエディターで内容を読み書きすることが可能だ。

Web ブラウザーで閲覧するべく HTML に変換することもある。それには [MkDocs] を用いる。Python が使用可能である端末エミュレーターがあればよい。

ノート執筆時点での私の環境は WSL 2 の Ubuntu 24.04.2 LTS だ。

Python 周りは次のとおりだが、詳しくは別ファイルで述べる：

* Python: 3.13.3
* MkDocs: 1.6.1

<!-- TODO: 問題点を記す。 -->

## リポジトリー構造

<!-- tree -a -d -I .git --dirsfirst -->

リポジトリーの `main` ブランチのディレクトリーのみの構造を次に示す：

```raw
.
├── .github
│   └── workflows
└── docs
    ├── community
    ├── context
    ├── css
    ├── design
    └── implementation
```

ルート直下には `mkdocs.yml` やプロジェクト管理に関係するファイル、その他を置く。

サブディレクトリー `.github/workflows` には GitHub Actions ワークフロー定義ファイルを置く。

サブディレクトリー `docs` 以下は [MkDocs] 既定の Markdown ファイル格納場所だ。本書の
Part それぞれに対応するサブディレクトリーを設けてある。

サブディレクトリー `docs/css` には MkDocs が生成するスタイルシートを調整するための CSS ファイルを置く。

## ビルド

[MkDocs] を用いて Markdown 原稿を HTML ファイルに変換する手順をファイル [INSTALL.md](./INSTALL.md) で述べる。

## 協力者

当ノートの執筆者を含む、プロジェクト協力者をファイル [CREDITS.md](./CREDITS.md) で述べる。

## 告知

ファイル `CHANGES`, `HISTORY`, `NEWS` のいずれかを設けるのが丁寧な仕事というものだ。
個人的なファイルなのでいずれも用意しないで済ませる気だ。

## メーリングリスト

個人プロジェクトにつき、開発者一同のメーリングリストや、それに準じるものは設けない。

[MkDocs]: <https://www.mkdocs.org/>
[TAOUP]: <http://www.catb.org/esr/writings/taoup/html/>
