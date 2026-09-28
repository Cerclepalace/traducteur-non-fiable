#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,re,sys
from pathlib import Path
SKIP={".git","__pycache__",".venv","venv","node_modules","outputs","artifacts","models",".cache","dist","build"}
BANNED=[re.compile(r"eleven\s*labs",re.I),re.compile(r"eleven_?labs",re.I),re.compile(r"api\.elevenlabs\.io",re.I),re.compile(r"xi[-_]api[-_]key",re.I)]
def walk(root):
 for dp,dn,fn in os.walk(root):
  dn[:]=[d for d in dn if d not in SKIP]
  for f in fn: yield Path(dp)/f
def main():
 p=argparse.ArgumentParser();p.add_argument("--root",default=".");p.add_argument("--json-out",default="inventory.json");a=p.parse_args();root=Path(a.root).resolve();hits=[];files=[]
 for f in walk(root):
  rel=f.relative_to(root).as_posix();files.append(rel)
  if f.suffix.lower() not in {".py",".md",".toml",".txt",".json",".yaml",".yml",".sh",".js",".ts",".env"}:continue
  try:lines=f.read_text(encoding="utf-8",errors="replace").splitlines()
  except OSError:continue
  for n,line in enumerate(lines,1):
   if "[HISTORICAL]" in line or "HISTORICAL-REFERENCE-OK" in line:continue
   if any(x.search(line) for x in BANNED):hits.append({"file":rel,"line":n,"text":line.strip()[:200]})
 r={"file_count":len(files),"elevenlabs_references":len(hits),"elevenlabs_hits":hits};Path(a.json_out).write_text(json.dumps(r,indent=2),encoding="utf-8");print(f"files={len(files)}");print(f"ELEVENLABS_REFERENCES={len(hits)}");return 1 if hits else 0
if __name__=="__main__":sys.exit(main())