# ddns

Python async ddns for cloudflare

feature:

- [x] update record only changed
-

## build

`pip install -r requirements.txt`

```
PYTHONOPTIMIZE=2 pyinstaller -F --clean --noupx --paths=$(`$PWD`) --python-option "-B -OO" -s -n pyddns main.py
```
