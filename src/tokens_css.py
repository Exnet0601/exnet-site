import json,sys
t=json.load(open(sys.argv[1]))
out=[":root{"]
for e in t['color']['tokens']:
    v=e['value']; v=v['light'] if isinstance(v,dict) else v
    out.append(f"  --{e['name']}:{v};")
for fam in ['spacing','radius','size','duration']:
    for e in t.get(fam,{}).get('tokens',[]): out.append(f"  --{e['name']}:{e['value']};")
for k,v in t['type']['families'].items(): out.append(f"  --font-{k}:{v};")
out.append("}")
print("\n".join(out))
