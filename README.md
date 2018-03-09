# pyessv-writer-amf

PYESSV vocab writer for AMF

## Usage

```
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Write the JSON vocabs to the local file system

```
python sh/write_amf_cvs.py --source=../AMF_CVs
```

Where: `../AMF_CVs` is the location on disk of the AMF CVs repository.

This should write the CV files locally to:

```
~/.esdoc/pyessv-archive/ncas/amf
```
