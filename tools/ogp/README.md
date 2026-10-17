# 共有画像（src/ogp.png）の作り方

1. `ogp.html` の文言を直す
2. 文言に使う文字だけの Noto Sans JP（500・700）を Google Fonts の `text=` 指定で取得し、`noto500.font`・`noto700.font` としてこのフォルダに置く
3. `chromium --headless --window-size=1200,800 --screenshot=raw.png ogp.html` で撮り、上から 1200×630 を切り出して `src/ogp.png` に保存する
