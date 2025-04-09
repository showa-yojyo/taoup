# Chapter 5. Textuality

[TOC]

<!-- ad-hoc: made or happening only for a particular purpose or need, not planned before it happens -->

> Interoperability, transparency, extensibility, and storage or transaction
> economy: these are the important themes in designing file formats and
> application protocols. Interoperability and transparency demand that we focus
> such designs on clean data representations, rather than putting convenience of
> implementation or highest possible performance first. Extensibility also
> favors textual protocols, since binary ones are often harder to extend or
> subset cleanly.

## The Importance of Being Textual

テキストストリームは、特別なツールを使わなくても、人間が簡単に読み書きや編集がで
きる。これらのフォーマットは透過的である（ように設計できる）。

> When you feel the urge to design a complex binary file format, or a complex
> binary application protocol, it is generally wise to lie down until the
> feeling passes.

バイナリー形式はダメだ。性能が心配なら、テキストストリームにアプリケーションプロ
トコルの下か上の階層で圧縮を施せばよいのだから。

> Binary formats usually specify the number of bits allocated to a given value,
> and extending them is difficult.

これは業務で経験がある。整数型として 32 ビットを勝手に想定していた時代のファイル
が 64 ビット時代になってダメになった。ファイルサイズをケチってかえって損をした。

バイナリー形式が本当に向いている場合は限定的だ：

> Formats for large images and multimedia are sometimes an example of the
> former, and network protocols with hard latency requirements sometimes an
> example of the latter.

バイナリー形式は拡張性に乏しいことにも注意。

> When you think you have an extreme case that justifies a binary file format or
> protocol, you need to think very carefully about extensibility and leaving
> room in the design for growth.

### Case Study: Unix Password File Format

ファイル `/etc/passwd` と等価な情報をバイナリー形式ファイルで置き換えるのは先述
の観点からも無理がある。本文ではこのファイルの場合に絞ってここで説明している。

テキスト形式であることの利点は例えば：

* 汎用テキストエディターで読み書き可能
* 汎用ツール (e.g. grep(1)) でテキスト内容を処理可能

CSV 形式を編集するときには、各欄に区切り記号を含めぬように注意しろ。

パスワードファイルはその用途上、バイナリー形式である利点が乏しい：

> Economy is not a major issue with password files to begin with, as they're
> normally read seldom and infrequently modified. Interoperability is not an
> issue, since various data in the file (notably user and group numbers) are not
> portable off the originating machine.

### Case Study: .newsrc Format

ファイル `.newsrc` についての考察。本書 Example 5.2 のコードを観察すると、これも
やはり可変長レコードを含む CSV の亜種だ。したがってバイナリー形式はダメ。

> The designers of the original newsreader chose transparency and
> interoperability over economy. The case for going in the other direction was
> not completely ridiculous; `.newsrc` files can get very large, and one modern
> reader (GNOME's Pan) uses a speed-optimized private format to avoid startup
> lag.

### Case Study: The PNG Graphics File Format

ここでバイナリー形式の例を見る。画像データをバイナリー形式で表現する理由が少なく
とも二つある：

> PNG is an excellent example of a thoughtfully designed binary format. A binary
> format is appropriate since graphics files may contain very large amounts of
> data, such that storage size and Internet download time would go up
> significantly if the pixel data were stored textually. Transaction economy was
> the prime consideration, with transparency sacrificed.

ちなみにここで言う transparency とは本書の意味でいうそれであり、画素の透明性とは
関係ない。PNG はアルファー値を扱う。

PNG 形式はチャンクやヘッダーの造りが良好であると述べる。著者の総評は次のとおり：

> The PNG standard is precise, comprehensive, and well written. It could serve
> as a model for how to write file format standards.

## Data File Metaformats

### DSV Style

### RFC 822 Format

### Cookie-Jar Format

### Record-Jar Format

### XML

### Windows INI Format

### Unix Textual File Format Conventions

### The Pros and Cons of File Compression

## Application Protocol Design

### Case Study: SMTP, the Simple Mail Transfer Protocol

### Case Study: POP3, the Post Office Protocol

### Case Study: IMAP, the Internet Message Access Protocol

## Application Protocol Metaformats

### The Classical Internet Application Metaprotocol

### HTTP as a Universal Application Protocol

### BEEP: Blocks Extensible Exchange Protocol

### XML-RPC, SOAP, and Jabber

