### 公式Docs
https://flet.dev/docs/

### github
https://github.com/flet-dev/flet

以下リンクに関する学習記事です。

https://flet.dev/docs/guides/python/getting-started

- cloudflare_pagesフォルダ
  - `main.py`:Publishing a static website
  - `runtime.txt`:PythonのVersion
  - `requirements.txt`：必要なライブラリ定義

- python_guideフォルダ
  - `auth.py`:Authentication
  - `storage.py`:Client storageとSession storage
  - `encrypt_decrypt.py`:Encrypting sensitive data
  - `package/packaging_desktop_app.py`:Packaging desktop app

```
flet run transper_pointer.py -d
```


# Controls
https://flet.dev/docs/controls/text/#using-system-fonts

### CloudFlare Workders
tsを選択する必要がないのかな？


### flyio
https://flet.dev/docs/guides/python/deploying-web-app/hosting-providers/fly-io


HTTPSConnectionPool(host='d1-tutorial.eno-conan.workers.dev', port=443): Max retries exceeded with url: /api/ (Caused by SSLError("Can't connect to HTTPS URL because the SSL module is not available."))

https://pypi.org/project/pyOpenSSL/
https://marusankakusikaku.jp/python/standard-library/urllib.request/

3.10.5

pyOpenSSL==23.2.0


git remote add origin https://github.com/eno-conan/Flet_cloudflare-workers-d1-sample.git