# Chapter 7. Multiprogramming

[TOC]

> The most characteristic program-modularization technique of Unix is splitting
> large programs into multiple cooperating processes.

ここでは cooperating に重点が置かれていると考える。

Unix はプログラムをより単純なサブプロセスに分割し、これらの間のインターフェイス
に集中することを奨励している。基本的な方法には次の三つがある：

* プロセス起動を安上がりなものにする
* プロセスが比較的かんたんに通信できるようにする方法（リダイレクト、パイプ、
  等々）を与える
* パイプやソケットを通して渡せる、単純で透過的なテキストデータ形式の使用を奨励す
  る

安価なプロセス起動と容易なプロセス制御は Unix 式のプログラミングを可能にする重要
な要素だ。

シェルでは、パイプで接続された複数のプロセス団をバックグラウンド、フォアグラウン
ド、その混合のどれであっても走らせることは比較的容易に設定可能だ。

プログラムを協調プロセスに分割することの利点と欠点：

* 大域的な複雑さを軽減する
* プロセス間の情報やコマンドの受け渡しに使われる通信規約の設計が難しい

> In software systems of all kinds, bugs collect at interfaces.

本当の課題は通信規格の構文ではなく論理、つまり、十分に表現力があり、膠着状態にな
らない規格を設計することだ。

## Separating Complexity Control from Performance Tuning

TODO: red herring

<!-- red herring: a fact, idea, or subject that takes people's attention away from the central point being considered -->

> Our discussion is *not* going to be about using concurrency to improve
> performance.

スレッドは大域的な複雑さを軽減するのではなく、むしろ増大させる。切実な必要性があ
る場合を除き、避けろ。

プログラムを協働プロセスに分割するもう一つの重要な理由は、より良い安全保障のため
だ：

* プログラムを setuid を必要とするプロセスとそれ以外の大きなプロセスに分割する。
* 前者は特権プロセスで、これだけが安全保障上重要なシステム資源へのアクセスが可能
  だ。
* 両プロセスを協働する。

脚注に setuid に関する補足がある：

> A setuid program runs not with the privileges of the user calling it, but with
> the privileges of the owner of the executable. This feature can be used to
> give restricted, program-controlled access to things like the password file
> that nonadministrators should not be allowed to modify directly.

## Taxonomy of Unix IPC Methods

### Handing off Tasks to Specialist Programs

### Pipes, Redirection, and Filters

### Wrappers

### Security Wrappers and Bernstein Chaining

### Slave Processes

### Peer-to-Peer Inter-Process Communication

## Problems and Methods to Avoid

### Obsolescent Unix IPC Methods

### Remote Procedure Calls

### Threads — Threat or Menace?

## Process Partitioning at the Design Level
