Backend
=======

```sh
uvicorn src.main:app --reload
```

or if you are put env under `env/`:
posix:
```sh
env/bin/python -m uvicorn src.main:app --reload
```
windows:
```ps
.\env\Scripts\python.exe -m uvicorn src.main:app --reload
```
