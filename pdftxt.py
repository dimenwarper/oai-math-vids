import sys, fitz
d = fitz.open(sys.argv[1]); a = int(sys.argv[2]) if len(sys.argv) > 2 else 0; b = int(sys.argv[3]) if len(sys.argv) > 3 else len(d)
print(f"[{len(d)} pages]")
for i in range(a, min(b, len(d))): print(f"--- p{i+1}\n" + d[i].get_text())
