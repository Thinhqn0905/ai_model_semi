"""Version-pinned Figshare downloader; archives are never executed."""
import argparse, hashlib, json, os, shutil, time, urllib.request, zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath

API = 'https://api.figshare.com/v2/articles/{}/versions/{}'

def resolve(article, version):
    with urllib.request.urlopen(API.format(article,version),timeout=30) as r: return json.load(r)

def hashes(path):
    md5=hashlib.md5(); sha=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''): md5.update(chunk); sha.update(chunk)
    return md5.hexdigest(),sha.hexdigest()

def verified(path, size, md5, sha256=None):
    if not path.is_file() or path.stat().st_size != size: return False
    m,s=hashes(path); return m.lower()==md5.lower() and (sha256 is None or s.lower()==sha256.lower())

def download(url, path, size, md5, sha256=None, retries=3, timeout=60):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if verified(path,size,md5,sha256): return hashes(path)
    part=path.with_name(path.name+'.part')
    for attempt in range(retries):
        try:
            offset=part.stat().st_size if part.exists() else 0
            if offset>size: part.unlink(); offset=0
            if shutil.disk_usage(path.parent).free < size-offset: raise OSError('insufficient disk space')
            request=urllib.request.Request(url,headers={'Range':f'bytes={offset}-'} if offset else {})
            with urllib.request.urlopen(request,timeout=timeout) as response:
                status=getattr(response,'status',200)
                if offset and status == 206:
                    if not response.headers.get('Content-Range','').startswith(f'bytes {offset}-'): raise ValueError('invalid Content-Range')
                    mode='ab'
                else: mode='wb'
                with part.open(mode) as f: shutil.copyfileobj(response,f,1024*1024)
            if not verified(part,size,md5,sha256):
                part.unlink(missing_ok=True); raise ValueError('size or digest mismatch')
            os.replace(part,path); return hashes(path)
        except (OSError,ValueError) as exc:
            if attempt+1==retries: raise
            time.sleep(min(2**attempt,4))

def safe_extract(archive, destination):
    dest=Path(destination).resolve()
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            name=item.filename.replace('\\','/'); p=PurePosixPath(name)
            if p.is_absolute() or PureWindowsPath(name).drive or '..' in p.parts or (item.external_attr >> 16) & 0o170000 == 0o120000: raise ValueError('unsafe zip member')
            if not (dest / name).resolve().is_relative_to(dest): raise ValueError('unsafe zip member')
        z.extractall(dest)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('article',type=int); ap.add_argument('version',type=int); ap.add_argument('out'); ap.add_argument('--sha256-json',help='JSON map of file name to expected SHA256'); args=ap.parse_args()
    metadata=resolve(args.article,args.version); out=Path(args.out); out.mkdir(parents=True,exist_ok=True); expected=json.loads(Path(args.sha256_json).read_text(encoding='utf8')) if args.sha256_json else {}; files=[]
    for f in metadata['files']:
        name=f['name']
        if Path(name).name!=name or not f.get('computed_md5'): raise ValueError('unsafe filename or missing checksum')
        m,s=download(f['download_url'],out/name,f['size'],f['computed_md5'],expected.get(name)); files.append({'name':name,'size':f['size'],'md5':m,'sha256':s,'url':f['download_url'],'sha256_expected':expected.get(name)})
    (out/'download_manifest.json').write_text(json.dumps({'article':args.article,'version':args.version,'doi':metadata.get('doi'),'files':files},indent=2),encoding='utf8')
if __name__=='__main__': main()
