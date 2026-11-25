import hashlib, io, importlib.util, zipfile
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('download_public_data',Path(__file__).resolve().parents[1]/'scripts/download_public_data.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def test_resume_and_skip(tmp_path, monkeypatch):
    data=b'abcdef'; target=tmp_path/'a'; (tmp_path/'a.part').write_bytes(data[:3]); calls=[]
    class Response(io.BytesIO):
        status=206
        headers={'Content-Range':'bytes 3-5/6'}
    def open_(req,timeout): calls.append(req.get_header('Range')); return Response(data[3:])
    monkeypatch.setattr(mod.urllib.request,'urlopen',open_)
    md5=hashlib.md5(data).hexdigest(); sha=hashlib.sha256(data).hexdigest()
    mod.download('https://example.test/a',target,6,md5,sha); assert target.read_bytes()==data and calls==['bytes=3-']
    mod.download('https://example.test/a',target,6,md5,sha); assert len(calls)==1

def test_unsafe_zip(tmp_path):
    z=tmp_path/'bad.zip'
    with zipfile.ZipFile(z,'w') as f: f.writestr('../outside','bad')
    with pytest.raises(ValueError): mod.safe_extract(z,tmp_path/'out')
