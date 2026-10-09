#!/usr/bin/env python3

import sys, os, re, io, json, zlib, base64, struct, zipfile, argparse, hashlib, secrets, tempfile, shutil
import subprocess, datetime, math
from array import array
from pathlib import Path

VERSION = '2.0'
SCRIPT_DIR = Path(__file__).resolve().parent
TOOLS_DIR = SCRIPT_DIR / 'tools'
MARKER = 'assets/fnglpatch.txt'
if array('I').itemsize != 4: raise SystemExit('this platform does not have 4-byte integers in array(I)')

def log(m=''): print(m, flush=True)

SIGDB = json.loads(zlib.decompress(base64.b64decode(
"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"
"ACvdROc=")).decode())


class Elf:
    def __init__(self, data):
        self.d = bytearray(data); d = self.d
        if d[:4] != b'\x7fELF' or d[4] != 2: raise ValueError('not a 64-bit ELF')
        if struct.unpack_from('<H', d, 0x12)[0] != 183: raise ValueError('not AArch64')
        self.phoff = struct.unpack_from('<Q', d, 0x20)[0]
        self.phentsize, self.phnum = struct.unpack_from('<HH', d, 0x36)
        self.loads = []
        for i in range(self.phnum):
            t, fl, o, va, pa, fsz, msz, al = struct.unpack_from('<IIQQQQQQ', d, self.phoff + i*self.phentsize)
            if t == 1: self.loads.append(dict(idx=i, off=o, va=va, fsz=fsz, msz=msz, fl=fl))
        ex = [l for l in self.loads if l['fl'] & 1]
        if not ex: raise ValueError('no executable segment')
        self.text_off, self.text_va, self.text_sz = ex[0]['off'], ex[0]['va'], ex[0]['fsz']
        rw = [l for l in self.loads if l['fl'] & 2]
        self.rw = max(rw, key=lambda l: l['va']) if rw else None
    def va2off(self, va):
        for l in self.loads:
            if l['va'] <= va < l['va'] + l['fsz']: return l['off'] + (va - l['va'])
        return None
    def words(self):
        if sys.byteorder != 'little': raise ValueError('a little-endian platform is required')
        n = self.text_sz // 4
        return memoryview(bytes(self.d[self.text_off:self.text_off + n*4])).cast('I')
    def wr(self, va, w):
        struct.pack_into('<I', self.d, self.va2off(va), w & 0xffffffff)


def sx(v, b): return v - (1 << b) if v & (1 << (b-1)) else v
def enc_b(frm, to, link=False):
    o = (to - frm) // 4
    if not -(1 << 25) <= o < (1 << 25) or (to - frm) % 4: raise ValueError('branch out of range')
    return (0x94000000 if link else 0x14000000) | (o & 0x3ffffff)
def enc_bcond(frm, to, cond):
    o = (to - frm) // 4
    if not -(1 << 18) <= o < (1 << 18): raise ValueError('b.cond out of range')
    return 0x54000000 | ((o & 0x7ffff) << 5) | cond
def enc_adrp(rd, pc, target):
    imm = (target >> 12) - (pc >> 12)
    if not -(1 << 20) <= imm < (1 << 20): raise ValueError('adrp fuera de rango')
    return 0x90000000 | ((imm & 3) << 29) | (((imm >> 2) & 0x7ffff) << 5) | rd
CMP_X_1000 = lambda rn: 0xF140041F | (rn << 5)                             
CSEL_LO    = lambda rt: 0x9A800000 | (rt << 16) | (3 << 12) | (17 << 5) | rt  
RET = 0xd65f03c0
def dec_imm19(w, pc): return pc + sx((w >> 5) & 0x7ffff, 19) * 4
def pc_relative(w):
    return ((w & 0x7C000000) == 0x14000000 or (w & 0xFF000010) == 0x54000000 or (w & 0x7E000000) == 0x34000000
            or (w & 0x7E000000) == 0x36000000 or (w & 0x1F000000) == 0x10000000 or (w & 0x3B000000) == 0x18000000)


_COMMON = {0xd65f03c0, 0xd503201f, 0x910003fd, 0xaa0003e0, 0xaa1f03e0, 0x2a1f03e0, 0xa9bf7bfd, 0xa8c17bfd, 0x52800000, 0x52800020,
           0x52800001, 0xaa0103e0, 0xaa0003e1, 0xf9400000, 0x910003e0, 0x2a0003e0, 0xd2800000}
def _seed_score(w):
    if w in _COMMON: return -10
    sc = 0
    if (w & 0x3B000000) == 0x39000000:                    
        off = ((w >> 10) & 0xfff) << (w >> 30)
        sc += 4 if off >= 0x40 else 1
    if (w & 0x7F800000) in (0x52800000, 0x72800000, 0x12800000): sc += 1
    if (w & 0xFFC00000) in (0xF1400000, 0x71400000, 0x91400000): sc += 2  
    sc += bin(w & 0xffff).count('1') // 6
    return sc

def find_sig(A, ws, ms, limit=16, lo=0, hi=None, tol=0):
    n = len(ws); hi = len(A) if hi is None else hi; raw = A.obj
    exact = [k for k in range(n) if ms[k] == 0xFFFFFFFF]
    if not exact: return []
    exact.sort(key=lambda k: -_seed_score(ws[k]))
    found = {}
    for k in exact[:tol + 1]:
        seed = struct.pack('<I', ws[k]); pos = (lo + k) * 4 - 1; hib = hi * 4
        while True:
            pos = raw.find(seed, pos + 1, hib)
            if pos < 0: break
            if pos & 3: continue
            i0 = pos // 4 - k
            if i0 < lo or i0 + n > hi or i0 in found: continue
            bad = 0
            for j in range(n):
                if (A[i0 + j] & ms[j]) != (ws[j] & ms[j]):
                    bad += 1
                    if bad > tol: break
            if bad <= tol:
                found[i0] = 1
                if len(found) >= limit: break
    return sorted(found)

def locate(A, ent, log):
    def sig_of(s): return [int(x, 16) for x in s['w']], [int(x, 16) for x in s['m']]
    big = [s for s in ent['sigs'] if s['b'] + s['a'] >= 12]
    small = [s for s in ent['sigs'] if s['b'] + s['a'] < 12]
    for s in big:
        ws, ms = sig_of(s); hits = find_sig(A, ws, ms)
        if len(hits) == s['n'] and s['n'] >= 1:
            return hits[s['i']] + s['b'], ('high' if s['b'] + s['a'] >= 20 else 'medium'), (s['b'], s['a'])
        if hits: log('   (window %d+%d ambigua: %d matches, expected %d)' % (s['b'], s['a'], len(hits), s['n']))
    for s in big:
        if s['n'] != 1: continue
        ws, ms = sig_of(s); hits = find_sig(A, ws, ms, tol=1)
        if len(hits) == 1: return hits[0] + s['b'], 'medium', (s['b'], s['a'])
    for s in small:
        ws, ms = sig_of(s); hits = find_sig(A, ws, ms)
        if len(hits) == s['n'] and s['n'] >= 1: return hits[s['i']] + s['b'], 'low', (s['b'], s['a'])
    return None


_PAD = re.compile(rb'(?:\x00\x00\x00\x00|\x1f\x20\x03\xd5){5,}')
class Caves:
    def __init__(self, elf, A):
        self.elf = elf; self.runs = []
        raw = bytes(elf.d[elf.text_off:elf.text_off + elf.text_sz])
        for m in _PAD.finditer(raw):
            s = ((m.start() + 3) & ~3) // 4
            while s*4 < m.end() and A[s] not in (0, 0xd503201f): s += 1
            e = s
            while e < len(A) and e*4 < m.end() + 4 and A[e] in (0, 0xd503201f): e += 1
            if e - s >= 5 and s > 0:
                p = A[s-1]
                term = (p == RET or (p & 0xFC000000) == 0x14000000 or (p & 0xFFFFFC1F) == 0xD61F0000)
                self.runs.append([s, e, term])
    def alloc(self, nwords, near_va):
        base = self.elf.text_va; best = None
        for strict in (True, False):
            for r in self.runs:
                if strict and not r[2]: continue
                if r[1] - r[0] < nwords: continue
                va = base + r[0] * 4; dist = abs(va - near_va)
                if dist >= (120 << 20): continue
                if best is None or dist < best[0]: best = (dist, r, va)
            if best: break
        if not best: raise RuntimeError('no padding space available for a %d-word code cave' % nwords)
        _, r, va = best; r[0] += nwords
        return va


def pick_zero_page(elf, A, mode, notes):
    rw = elf.rw
    if rw is None: raise RuntimeError('ELF has no data segment')
    end = rw['va'] + rw['msz']
    if mode == 'extend':
        zp = (end + 0xfff) & ~0xfff
        po = elf.phoff + rw['idx'] * elf.phentsize
        struct.pack_into('<Q', elf.d, po + 0x28, (zp + 0x1000) - rw['va'])
        notes.append('extended BSS: memsz %#x -> %#x, zero page at %#x' % (rw['msz'], (zp + 0x1000) - rw['va'], zp))
        return zp
    bss_lo = rw['va'] + rw['fsz']; lo, hi = bss_lo >> 12, end >> 12; base = elf.text_va; refs = set()
    for i, w in enumerate(A):
        if (w & 0x9F000000) == 0x90000000:
            imm = (((w >> 5) & 0x7ffff) << 2) | ((w >> 29) & 3)
            if imm & (1 << 20): imm -= 1 << 21
            p = ((base + i*4) >> 12) + imm
            if lo <= p <= hi: refs.add(p)
    gaps = []; prev = lo
    for p in sorted(refs) + [hi + 1]:
        if p - prev >= 8: gaps.append((prev, p))
        prev = p + 1
    if not gaps: raise RuntimeError('no free .bss gap; use --zp extend')
    zp = (gaps[-1][0] + 1) << 12
    notes.append('zero page (gap) at %#x' % zp)
    return zp


def patch_lib(data, zp_mode, log, dry=False):
    elf = Elf(data); A = elf.words(); base = elf.text_va
    caves = Caves(elf, A); notes = []
    zp = pick_zero_page(elf, A, zp_mode, notes) if not dry else 0
    for n in notes: log('  ' + n)
    found = {}; missing = []
    for ent in SIGDB:
        r = locate(A, ent, log)
        if r is None: missing.append(ent['id']); log('  [--] %-18s not found' % ent['id']); continue
        found[ent['id']] = (r[0], r[1])
        log('  [ok] %-18s %#x  (confidence %s, window %d+%d)' % (ent['id'], base + r[0]*4, r[1], r[2][0], r[2][1]))
    if dry: return None, found, missing
    W = lambda va: A[(va - base)//4]
    skipped = []
    for ent in SIGDB:
        if ent['id'] not in found: continue
        va = base + found[ent['id']][0] * 4; w = W(va); k = ent['kind']
        try:
            if k == 'fatal_skip':
                if (w & 0xFC000000) != 0x94000000: raise ValueError('site is not a bl')
                tgt = None; si = (va - base)//4
                lo = max(0, si - 0x300); hi = min(len(A), si + 0x300)
                for ts in ent['tsigs']:
                    ws = [int(x, 16) for x in ts['w']]; ms = [int(x, 16) for x in ts['m']]
                    hits = find_sig(A, ws, ms, lo=lo, hi=hi)
                    if len(hits) == 1:
                        cand = base + (hits[0] + ts['b']) * 4
                        if cand > va and cand - va < 0x800: tgt = cand; break
                if tgt is None: raise ValueError('continuation not found')
                elf.wr(va, enc_b(va, tgt))
            elif k == 'mov_w1_0':
                if (w & 0xFFC003E0) != 0xB9400100 or (w & 31) != 1: raise ValueError('unexpected instruction %08x' % w)
                elf.wr(va, 0x52800001)
            elif k == 'cbz_to_b':
                if (w & 0xFF000000) != 0xB4000000: raise ValueError('not cbz x')
                elf.wr(va, enc_b(va, dec_imm19(w, va)))
            elif k in ('guard_cbz', 'guard_cbnz'):
                rn = w & 31
                if k == 'guard_cbz':
                    if (w & 0xFF000000) != 0xB4000000: raise ValueError('not cbz x')
                    ld_va = va + 4; ret = va + 8; other = dec_imm19(w, va)
                else:
                    if (w & 0xFF000000) != 0xB5000000: raise ValueError('not cbnz x')
                    ld_va = dec_imm19(w, va); ret = ld_va + 4; other = va + 4
                ld = W(ld_va)
                if pc_relative(ld): raise ValueError('PC-relative load instruction')
                c = caves.alloc(5, va)
                words = [CMP_X_1000(rn), enc_bcond(c + 4, c + 16, 3), ld, enc_b(c + 12, ret), enc_b(c + 16, other)]
                for i, x in enumerate(words): elf.wr(c + 4*i, x)
                elf.wr(va, enc_b(va, c))
            elif k == 'entry_guard':
                if pc_relative(w): raise ValueError('first instruction is PC-relative')
                c = caves.alloc(5, va)
                words = [CMP_X_1000(1), enc_bcond(c + 4, c + 16, 3), w, enc_b(c + 12, va + 4), RET]
                for i, x in enumerate(words): elf.wr(c + 4*i, x)
                elf.wr(va, enc_b(va, c))
            elif k == 'sanitize':
                rt = ent['rt']
                if (w & 31) != rt or pc_relative(w): raise ValueError('unexpected instruction %08x' % w)
                c = caves.alloc(5, va)
                words = [w, CMP_X_1000(rt), enc_adrp(17, c + 8, zp), CSEL_LO(rt), enc_b(c + 16, va + 4)]
                for i, x in enumerate(words): elf.wr(c + 4*i, x)
                elf.wr(va, enc_b(va, c))
        except Exception as e:
            skipped.append((ent['id'], str(e))); log('  [!!] %-18s %s' % (ent['id'], e))
    return bytes(elf.d), found, missing + [s[0] for s in skipped]






def _mk_len():
    L = {}
    for o in [0x00,0x01,0x04,0x07,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x10,0x11,0x1d,0x1e,0x21,0x27,0x28] + list(range(0x7b,0x90)) + list(range(0xb0,0xd0)): L[o] = 1
    for o in [0x02,0x05,0x08,0x13,0x15,0x16,0x19,0x1a,0x1c,0x1f,0x20,0x22,0x23,0x29,0x2d,0x2e,0x2f,0x30,0x31] + list(range(0x32,0x3e)) + list(range(0x44,0x6e)) + list(range(0xd0,0xe3)): L[o] = 2
    for o in [0x03,0x06,0x09,0x14,0x17,0x1b,0x24,0x25,0x26,0x2a,0x2b,0x2c] + list(range(0x6e,0x73)) + list(range(0x74,0x79)) + [0xfa,0xfb,0xfc,0xfd]: L[o] = 3
    L[0x18] = 5; L[0xfe] = 2; L[0xff] = 2
    for o in range(0x3e,0x44): L[o] = 1
    return L
_DEX_LEN = _mk_len()

class Dex:
    def __init__(self, d):
        self.d = bytearray(d)
        if self.d[:4] != b'dex\n': raise ValueError('not a DEX file')
        (self.ssz, self.soff, self.tsz, self.toff, self.psz, self.poff, self.fsz, self.foff,
         self.msz, self.moff, self.csz, self.coff) = struct.unpack_from('<12I', self.d, 0x38)
    def uleb(self, o):
        r = 0; s = 0
        while True:
            b = self.d[o]; o += 1; r |= (b & 0x7f) << s; s += 7
            if not b & 0x80: return r, o
    def string(self, i):
        off = struct.unpack_from('<I', self.d, self.soff + 4*i)[0]; ln, o = self.uleb(off)
        return bytes(self.d[o:o+ln]).decode('utf-8', 'replace')
    def type(self, i): return self.string(struct.unpack_from('<I', self.d, self.toff + 4*i)[0])
    def method(self, i):
        c, p, n = struct.unpack_from('<HHI', self.d, self.moff + 8*i); return self.type(c), self.string(n), p
    def ret_type(self, pidx):
        sh, rt, po = struct.unpack_from('<III', self.d, self.poff + 12*pidx); return self.type(rt)
    def defined(self):
        out = {}
        for i in range(self.csz):
            cidx, acc, sup, ifc, src, ann, cd, sv = struct.unpack_from('<8I', self.d, self.coff + 32*i)
            out[self.type(cidx)] = cd
        return out
    def methods_of(self, cd):
        if not cd: return
        o = cd; sf, o = self.uleb(o); inf, o = self.uleb(o); dm, o = self.uleb(o); vm, o = self.uleb(o)
        for _ in range(sf + inf): _, o = self.uleb(o); _, o = self.uleb(o)
        for cnt in (dm, vm):
            idx = 0
            for _ in range(cnt):
                di, o = self.uleb(o); acc, o = self.uleb(o); code, o = self.uleb(o); idx += di
                yield idx, acc, code
    def fix_header(self):
        d = self.d
        d[12:32] = hashlib.sha1(bytes(d[32:])).digest()
        struct.pack_into('<I', d, 8, zlib.adler32(bytes(d[12:])) & 0xffffffff)

def patch_dex_set(dexes, log):
    parsed = {}
    for n, b in dexes.items():
        try: parsed[n] = Dex(b)
        except Exception as e: log('  unreadable DEX %s: %s' % (n, e))
    defined = set()
    for D in parsed.values(): defined |= set(D.defined().keys())
    out = {}
    for name, D in parsed.items():
        for cname, cd in D.defined().items():
            if cname != 'Lcom/epicgames/ue4/GameActivity;': continue
            for idx, acc, code in D.methods_of(cd):
                c, mname, pidx = D.method(idx)
                if mname != 'DownloadConfigRules' or D.ret_type(pidx) != 'Z' or not code: continue
                regs, ins, outs, tries, dbg, isz = struct.unpack_from('<HHHHII', D.d, code)
                if regs < 1 or isz < 2: log('  [!!] dex: DownloadConfigRules has insufficient registers'); continue
                missing = set(); i = 0; st = code + 16
                while i < isz:
                    u = struct.unpack_from('<H', D.d, st + 2*i)[0]; op = u & 0xff
                    if u in (0x0100, 0x0200, 0x0300): break
                    if op == 0x22: missing.add(D.type(struct.unpack_from('<H', D.d, st + 2*i + 2)[0]))
                    i += _DEX_LEN.get(op, 1)
                missing = {t for t in missing if t not in defined and t.startswith('Lcom/epicgames/')}
                if not missing:
                    log('  dex %s: DownloadConfigRules does not instantiate missing classes; no changes' % name); continue
                struct.pack_into('<HH', D.d, st, 0x1012, 0x000f)      
                D.fix_header(); out[name] = bytes(D.d)
                log('  [ok] dex %s: DownloadConfigRules -> return true (missing class: %s)' % (name, ', '.join(sorted(missing))))
    return out


def patch_cmdline(txt, nomcp, execcmds):
    t = txt.rstrip('\r\n')
    if nomcp is None: nomcp = not re.search(r'-AUTH_', t)        
    if nomcp and not re.search(r'(^|\s)-nomcp(\s|$)', t): t += ' -nomcp'
    if execcmds:
        cmd = 'r.ProgramBinaryCache.Enable 0'
        m = re.search(r'-ExecCmds="([^"]*)"', t, re.I)
        if m:
            if cmd not in m.group(1): t = t[:m.start(1)] + (m.group(1) + ',' if m.group(1) else '') + cmd + t[m.end(1):]
        else: t += ' -ExecCmds="%s"' % cmd
    return t


def write_apk(src, dst, replace, extra_files=None):
    zi = zipfile.ZipFile(src); out = zipfile.ZipFile(dst, 'w')
    names = set()
    for i in zi.infolist():
        n = i.filename
        if n.startswith('META-INF/') and not n.endswith('/'): continue     
        data = replace.get(n)
        if data is None: data = zi.read(n)
        zf = zipfile.ZipInfo(n, date_time=i.date_time)
        zf.compress_type = i.compress_type; zf.external_attr = i.external_attr
        if i.compress_type == 0:
            al = 4096 if n.endswith('.so') else 4
            zf.extra = b'\x00' * ((-(out.fp.tell() + 30 + len(n.encode()))) % al)
        out.writestr(zf, data); names.add(n)
    for n, data in (extra_files or {}).items():
        if n in names: continue
        zf = zipfile.ZipInfo(n, date_time=(2026, 1, 1, 0, 0, 0)); zf.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(zf, data)
    out.close()


def _is_prime(n, rounds=32):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
        if n % p == 0: return n == p
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2; x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def _gen_prime(bits):
    while True:
        p = secrets.randbits(bits) | (1 << (bits - 1)) | (1 << (bits - 2)) | 1
        if _is_prime(p): return p
def gen_rsa(bits=2048):
    e = 65537
    while True:
        p = _gen_prime(bits // 2); q = _gen_prime(bits // 2)
        if p == q: continue
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) != 1: continue
        n = p * q
        if n.bit_length() != bits: continue
        return n, e, pow(e, -1, phi)

def _len(n): return bytes([n]) if n < 128 else (b'\x81' + bytes([n]) if n < 256 else (b'\x82' + n.to_bytes(2, 'big') if n < 65536 else b'\x83' + n.to_bytes(3, 'big')))
def _der(tag, c): return bytes([tag]) + _len(len(c)) + c
def _int(i): b = i.to_bytes((i.bit_length() + 8) // 8 or 1, 'big'); return _der(0x02, b)
def _oid(s):
    a = [int(x) for x in s.split('.')]; out = bytes([a[0] * 40 + a[1]])
    for v in a[2:]:
        chunk = [v & 0x7f]; v >>= 7
        while v: chunk.append((v & 0x7f) | 0x80); v >>= 7
        out += bytes(reversed(chunk))
    return _der(0x06, out)
_NULL = b'\x05\x00'
_SHA256_RSA = _der(0x30, _oid('1.2.840.113549.1.1.11') + _NULL)
_SHA256_PREFIX = bytes.fromhex('3031300d060960864801650304020105000420')

def rsa_sign(n, d, msg):
    t = _SHA256_PREFIX + hashlib.sha256(msg).digest(); k = (n.bit_length() + 7) // 8
    em = b'\x00\x01' + b'\xff' * (k - len(t) - 3) + b'\x00' + t
    return pow(int.from_bytes(em, 'big'), d, n).to_bytes(k, 'big')

def make_cert(n, e, d, cn='Fortnite GL Patch'):
    name = _der(0x30, _der(0x31, _der(0x30, _oid('2.5.4.3') + _der(0x0c, cn.encode()))))
    spki = _der(0x30, _der(0x30, _oid('1.2.840.113549.1.1.1') + _NULL) + _der(0x03, b'\x00' + _der(0x30, _int(n) + _int(e))))
    validity = _der(0x30, _der(0x17, b'200101000000Z') + _der(0x17, b'491231235959Z'))
    tbs = _der(0x30, _der(0xa0, _int(2)) + _int(secrets.randbits(63) | 1) + _SHA256_RSA + name + validity + name + spki)
    sig = rsa_sign(n, d, tbs)
    return _der(0x30, tbs + _SHA256_RSA + _der(0x03, b'\x00' + sig)), spki

def load_key(path_hint=None):
    kf = TOOLS_DIR / 'fnpatch_debug_key.json'
    try:
        if kf.exists():
            j = json.loads(kf.read_text()); return int(j['n'], 16), int(j['e'], 16), int(j['d'], 16), base64.b64decode(j['cert']), base64.b64decode(j['spki'])
    except Exception: pass
    log('  generating RSA-2048 signing key (first run only; this may take a few seconds) ...')
    n, e, d = gen_rsa(2048); cert, spki = make_cert(n, e, d)
    try:
        TOOLS_DIR.mkdir(parents=True, exist_ok=True)
        kf.write_text(json.dumps(dict(n='%x' % n, e='%x' % e, d='%x' % d, cert=base64.b64encode(cert).decode(), spki=base64.b64encode(spki).decode())))
        log('  key saved to %s (reused to allow in-place updates)' % kf)
    except Exception as ex: log('  (could not save key: %s)' % ex)
    return n, e, d, cert, spki

def _lp(b): return struct.pack('<I', len(b)) + b
def _find_eocd(data):
    i = data.rfind(b'PK\x05\x06', max(0, len(data) - 0x10000 - 22))
    if i < 0: raise ValueError('EOCD not found')
    return i
def _chunk_digest(sections):
    digs = []; total = 0
    for sec in sections:
        mv = memoryview(sec)
        for o in range(0, len(sec), 1 << 20):
            ch = mv[o:o + (1 << 20)]
            digs.append(hashlib.sha256(b'\xa5' + struct.pack('<I', len(ch)) + ch).digest()); total += 1
    return hashlib.sha256(b'\x5a' + struct.pack('<I', total) + b''.join(digs)).digest()

def sign_v2(in_path, out_path, key):
    n, e, d, cert, spki = key
    data = Path(in_path).read_bytes()
    eo = _find_eocd(data)
    cd_size, cd_off = struct.unpack_from('<II', data, eo + 12)
    if data[cd_off - 16:cd_off] == b'APK Sig Block 42': raise ValueError('APK already has a signature block')
    sec1 = data[:cd_off]; sec2 = data[cd_off:cd_off + cd_size]; sec3 = data[eo:]
    digest = _chunk_digest([sec1, sec2, sec3])
    algo = 0x0103
    digests_seq = _lp(struct.pack('<I', algo) + _lp(digest))
    certs_seq = _lp(cert)
    signed_data = _lp(digests_seq) + _lp(certs_seq) + _lp(b'')
    signature = rsa_sign(n, d, signed_data)
    sigs_seq = _lp(struct.pack('<I', algo) + _lp(signature))
    signer = _lp(signed_data) + _lp(sigs_seq) + _lp(spki)
    value = _lp(_lp(signer))
    pair = struct.pack('<Q', 4 + len(value)) + struct.pack('<I', 0x7109871a) + value
    block = struct.pack('<Q', len(pair) + 8 + 16) + pair + struct.pack('<Q', len(pair) + 8 + 16) + b'APK Sig Block 42'
    eocd = bytearray(sec3); struct.pack_into('<I', eocd, 16, cd_off + len(block))
    with open(out_path, 'wb') as f:
        f.write(sec1); f.write(block); f.write(sec2); f.write(eocd)

def verify_v2(path):
    data = Path(path).read_bytes(); eo = _find_eocd(data)
    cd_size, cd_off = struct.unpack_from('<II', data, eo + 12)
    if data[cd_off - 16:cd_off] != b'APK Sig Block 42': return False, 'no signature block'
    bsz = struct.unpack_from('<Q', data, cd_off - 24)[0]; bstart = cd_off - bsz - 8
    if struct.unpack_from('<Q', data, bstart)[0] != bsz: return False, 'inconsistent block size'
    o = bstart + 8; end = cd_off - 24; value = None
    while o < end:
        ln = struct.unpack_from('<Q', data, o)[0]; pid = struct.unpack_from('<I', data, o + 8)[0]
        if pid == 0x7109871a: value = data[o + 12:o + 8 + ln]
        o += 8 + ln
    if value is None: return False, 'no v2 block'
    def rd(buf, off):
        l = struct.unpack_from('<I', buf, off)[0]; return buf[off + 4:off + 4 + l], off + 4 + l
    signers, _ = rd(value, 0); signer, _ = rd(signers, 0)
    signed_data, p = rd(signer, 0); sigs, p = rd(signer, p); spki, p = rd(signer, p)
    ds, q = rd(signed_data, 0); dig_rec, _ = rd(ds, 0); algo = struct.unpack_from('<I', dig_rec, 0)[0]; dig, _ = rd(dig_rec, 4)
    sig_rec, _ = rd(sigs, 0); salgo = struct.unpack_from('<I', sig_rec, 0)[0]; sig, _ = rd(sig_rec, 4)
    if algo != 0x0103 or salgo != 0x0103: return False, 'unsupported algorithm %x' % algo
    sec1 = data[:bstart]; sec2 = data[cd_off:cd_off + cd_size]; sec3 = bytearray(data[eo:]); struct.pack_into('<I', sec3, 16, bstart)
    if _chunk_digest([sec1, sec2, bytes(sec3)]) != dig: return False, 'APK digest does not match'
   
    def der_read(b, o):
        l = b[o + 1]
        if l < 128: return b[o], o + 2, l
        nb = l & 0x7f; return b[o], o + 2 + nb, int.from_bytes(b[o + 2:o + 2 + nb], 'big')
    t, off, l = der_read(spki, 0)                      
    t, o1, l1 = der_read(spki, off); o1 += l1          
    t, o2, l2 = der_read(spki, o1)                     
    rsa = spki[o2 + 1:o2 + l2]
    t, o3, l3 = der_read(rsa, 0)                       
    t, o4, l4 = der_read(rsa, o3); nmod = int.from_bytes(rsa[o4:o4 + l4], 'big')
    t, o5, l5 = der_read(rsa, o4 + l4); ee = int.from_bytes(rsa[o5:o5 + l5], 'big')
    kk = (nmod.bit_length() + 7) // 8
    em = pow(int.from_bytes(sig, 'big'), ee, nmod).to_bytes(kk, 'big')
    want = b'\x00\x01' + b'\xff' * (kk - len(_SHA256_PREFIX) - 32 - 3) + b'\x00' + _SHA256_PREFIX + hashlib.sha256(signed_data).digest()
    if em != want: return False, 'RSA signature is invalid'
    return True, 'valid v2 signature (RSA-%d, SHA-256)' % nmod.bit_length()


UBER_URL = 'https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar'
def sign_with_uber(unsigned, final):
    if not shutil.which('java'): raise RuntimeError('Java is not installed (use --signer builtin)')
    jars = sorted(TOOLS_DIR.glob('uber-apk-signer*.jar')) + sorted(SCRIPT_DIR.glob('uber-apk-signer*.jar'))
    if jars: jar = jars[-1]
    else:
        import urllib.request
        TOOLS_DIR.mkdir(parents=True, exist_ok=True); jar = TOOLS_DIR / UBER_URL.rsplit('/', 1)[1]
        log('  downloading %s ...' % jar.name)
        with urllib.request.urlopen(UBER_URL, timeout=120) as r, open(jar, 'wb') as f: shutil.copyfileobj(r, f)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(['java', '-jar', str(jar), '-a', str(unsigned), '-o', tmp, '--allowResign'],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        outs = sorted(Path(tmp).glob('*.apk'))
        if r.returncode or not outs: raise RuntimeError('uber-apk-signer failed:\n' + r.stdout[-1500:])
        shutil.move(str(outs[0]), str(final))


def apk_info(apk):
    zi = zipfile.ZipFile(apk); libs = {}
    for n in zi.namelist():
        m = re.fullmatch(r'lib/([^/]+)/(libUE4\.so)', n)
        if m: libs[m.group(1)] = n
    return zi, libs

def pick_apk_interactively():
    folders = [SCRIPT_DIR] + ([Path.cwd()] if Path.cwd() != SCRIPT_DIR else [])
    cands = []
    for f in folders:
        for p in sorted(f.glob('*.apk')):
            if not re.search(r'(_fixed|_unsigned)\.apk$', p.name, re.I) and p not in cands: cands.append(p)
    log('=' * 70); log(' fortnite_gl_autopatch %s - Fortnite UE4 (OpenGL ES sobre ANGLE) en Android arm64' % VERSION); log('=' * 70)
    log('Place the APK in this folder: %s' % SCRIPT_DIR)
    if cands:
        log('APKs found:')
        for i, p in enumerate(cands, 1): log('  [%d] %s' % (i, p.name))
    else: log('(there are no .apk files in this folder yet)')
    while True:
        default = ' [Enter = %s]' % cands[0].name if len(cands) == 1 else ''
        try: ans = input('\nAPK name (or number)%s: ' % default).strip().strip('"')
        except EOFError: sys.exit('No input.')
        if not ans and len(cands) == 1: return cands[0]
        if not ans: continue
        if ans.isdigit() and 1 <= int(ans) <= len(cands): return cands[int(ans) - 1]
        if Path(ans).is_file(): return Path(ans)
        for f in folders:
            for name in (ans, ans + '.apk'):
                if (f / name).is_file(): return f / name
        log("  '%s' was not found in %s. Try again." % (ans, SCRIPT_DIR))

def process_apk(apk, a):
    log('\nInput: %s (%.1f MB)' % (apk.name, apk.stat().st_size / 1e6))
    zi, libs = apk_info(apk)
    if MARKER in zi.namelist() and not a.force:
        log('This APK has already been patched by fortnite_gl_autopatch (use --force to run again).'); return 0
    if not libs:
        log('ERROR: the APK does not contain lib/*/libUE4.so; it is not a native Fortnite UE4 APK.'); return 2
    if 'arm64-v8a' not in libs:
        log('ERROR: the APK only contains code for %s, not arm64-v8a.' % ', '.join(sorted(libs)))
        log('       The Galaxy A57 is arm64: it would not install (INSTALL_FAILED_NO_MATCHING_ABIS), and this cannot be patched.')
        return 2
    replace = {}; total_missing = 0
    for abi, name in libs.items():
        if abi != 'arm64-v8a': log('  (skipping %s: only arm64-v8a is patched)' % name); continue
        data = zi.read(name); log('\n[1/4] %s (%.1f MB): searching for signature matches ...' % (name, len(data) / 1e6))
        newd, found, missing = patch_lib(data, a.zp, log, a.dry_run)
        total_missing += len(missing)
        log('  summary: %d/%d patches located, %d not applied' % (len(found), len(SIGDB), len(missing)))
        if newd is not None: replace[name] = newd
    if a.dry_run: log('\n(dry-run: nothing was written)'); return 0
    if a.require_all and total_missing:
        log('ERROR: patches are missing and --require-all was specified.'); return 3
    if total_missing == len(SIGDB):
        log('\nERROR: no patch points were recognized; this libUE4.so version is not supported.'); return 3
    log('\n[2/4] classes.dex and command line ...')
    if not a.no_dex_fix:
        dexes = {n: zi.read(n) for n in zi.namelist() if re.fullmatch(r'classes\d*\.dex', n)}
        if dexes: replace.update(patch_dex_set(dexes, log))
    cl = 'assets/UE4CommandLine.txt'
    if cl in zi.namelist():
        old = zi.read(cl).decode('utf-8', 'replace'); new = patch_cmdline(old, a.nomcp, not a.no_execcmds)
        replace[cl] = new.encode('utf-8'); log('  UE4CommandLine: ' + new.replace('\n', ' | '))
    suffix = '_unsigned.apk' if a.no_sign else '_fixed.apk'
    out = Path(a.out) if a.out else apk.with_name(apk.stem + suffix)
    with tempfile.TemporaryDirectory() as tmp:
        built = Path(tmp) / 'built.apk'
        log('\n[3/4] rebuilding APK (aligned to 4 bytes / 4 KB for .so files) ...')
        write_apk(apk, built, replace, {MARKER: ('fortnite_gl_autopatch %s\n' % VERSION).encode()})
        if a.no_sign: shutil.copy(built, out); log('[4/4] signing skipped (--no-sign)')
        elif a.signer == 'uber':
            log('[4/4] signing with uber-apk-signer (Java) ...'); sign_with_uber(built, out)
        else:
            log('[4/4] signing (v2 scheme, pure Python) ...'); sign_v2(built, out, load_key())
            ok, msg = verify_v2(out); log('  verification: ' + msg)
            if not ok: log('ERROR: the generated signature failed verification; do not install this APK.'); return 4
    log('\n' + '=' * 70); log('DONE: %s' % out); log('=' * 70)
    log('Next steps:')
    log('  1. Uninstall the original Fortnite app (the signature is different).')
    log('  2. Install %s (copy it to your phone or run: adb install "%s").' % (out.name, out))
    if not a.no_sign and a.signer != 'uber': log('  (Signed with a custom debug key; suitable for manual installation.)')
    if a.install:
        if not shutil.which('adb'): log('  --install: adb is not in PATH.')
        else:
            r = subprocess.run(['adb', 'install', '-r', str(out)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log('  adb: ' + r.stdout.strip()[-400:])
    return 0

def process_lib(path, a):
    data = Path(path).read_bytes(); log('== %s (%.1f MB)' % (Path(path).name, len(data) / 1e6))
    newd, found, missing = patch_lib(data, a.zp, log, a.dry_run)
    log('  summary: %d/%d patches located, %d not applied' % (len(found), len(SIGDB), len(missing)))
    if newd is None: return 0
    out = Path(a.out) if a.out else Path(str(path) + '.patched'); out.write_bytes(newd); log('written: %s' % out); return 0

def main():
    ap = argparse.ArgumentParser(description='One-click patcher for Fortnite UE4 (OpenGL ES over ANGLE) on Android arm64')
    ap.add_argument('input', nargs='?', help=' .apk or libUE4.so (optional; prompts if omitted)')
    ap.add_argument('-o', '--out', '--output', dest='out')
    ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--no-sign', action='store_true')
    g = ap.add_mutually_exclusive_group(); g.add_argument('--nomcp', dest='nomcp', action='store_true', default=None)
    g.add_argument('--no-nomcp', dest='nomcp', action='store_false')
    ap.add_argument('--no-execcmds', action='store_true'); ap.add_argument('--no-dex-fix', action='store_true')
    ap.add_argument('--zp', choices=('extend', 'gap'), default='extend')
    ap.add_argument('--require-all', action='store_true'); ap.add_argument('--force', action='store_true')
    ap.add_argument('--signer', choices=('builtin', 'uber'), default='builtin')
    ap.add_argument('--install', action='store_true'); ap.add_argument('--verify', metavar='APK')
    a = ap.parse_args()
    if a.verify:
        ok, msg = verify_v2(a.verify); log(('OK: ' if ok else 'FAILED: ') + msg); sys.exit(0 if ok else 1)
    interactive = a.input is None; code = 0
    try:
        src = pick_apk_interactively() if interactive else Path(a.input)
        if not src.exists(): sys.exit('Does not exist: %s' % src)
        raw = src.open('rb').read(4)
        if raw[:2] == b'PK': code = process_apk(src, a)
        elif raw == b'\x7fELF': code = process_lib(src, a)
        else: sys.exit('Input must be an .apk or libUE4.so')
    except SystemExit as e:
        if interactive and e.code not in (None, 0):
            if isinstance(e.code, str): print(e.code)
            _pause(interactive); sys.exit(1)
        raise
    except Exception as e:
        log('\nERROR: %s' % e)
        if interactive: _pause(interactive)
        sys.exit(1)
    _pause(interactive); sys.exit(code)

def _pause(interactive):
    if interactive and sys.stdin.isatty():
        try: input('\nPress Enter to exit...')
        except EOFError: pass

if __name__ == '__main__':
    main()
