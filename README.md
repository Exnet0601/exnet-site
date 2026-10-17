# exnet.biz コーポレートサイト

`src/build.py` が `site/` に HTML と CSS を書き出す静的サイトです。

```
python3 src/build.py
```

- 文章とページ構成は `src/build.py`、見た目は `src/site.css`（デザインシステム「エクスネット」の部品は `src/bundle.css`、色や余白は `src/tokens.json`）。
- Claude の Artifact で確認用に出すときは `SITE_ARTIFACT=1 python3 src/build.py`（トップページを本文だけで書き出す）。
- `main` に取り込まれると、GitHub Actions が組み立てて、ロリポップへ FTP でアップロードします（`.github/workflows/deploy.yml`）。
- アップロード先のフォルダは Secrets の `FTP_SERVER_DIR` で決まります。公開前は確認用のフォルダ、公開日に `/` に切り替えます。
