"""Exact constructors and event simulation for switching-budget hysteron machines.

Python 3.10+, standard library only. Thresholds are integer-scaled by 8*(n+1).
A complete input pulse rises from L to H and then returns to L. The simulator
allows at most one individual flip on each half and checks post-event stability.
"""
from __future__ import annotations
from itertools import combinations
from math import comb


def require(test: bool, message: str) -> None:
    if not test:
        raise ValueError(message)


def validate_map(f: list[int]) -> None:
    require(bool(f), 'The logical state set must be nonempty')
    require(all(type(j) is int and 0 <= j < len(f) for j in f), 'Invalid successor')


def has_two_cycle(f: list[int]) -> bool:
    validate_map(f)
    return any(j != i and f[j] == i for i, j in enumerate(f))


def one_hot(f: list[int], gates: list[int] | None = None,
            alphabet_size: int = 1) -> dict:
    """Realize any unary map without 2-cycles, or its nested amplitude gates.

    Logical i is the configuration 1<<i. Gate g_i is the first active amplitude,
    numbered 1..alphabet_size. Both threshold branches share one nonnegative
    affine shift and have the same hysteresis width. Global bands are separated.
    """
    validate_map(f)
    require(not has_two_cycle(f), 'A two-cycle is forbidden by the switching budget')
    n = len(f); r = alphabet_size
    require(type(r) is int and r >= 1, 'Invalid alphabet size')
    gates = [1]*n if gates is None else list(gates)
    require(len(gates) == n and all(type(g) is int and 1 <= g <= r for g in gates),
            'Invalid activation gates')
    J = [[0 if i == j else 2*r+1 for j in range(n)] for i in range(n)]
    for i, j in enumerate(f):
        if i != j:
            J[j][i] = 2*gates[i]-1
            J[i][j] = 2*r+3
    B = max(map(sum, J), default=0)+1
    D = 8*(n+1)
    return {'kind':'affine','n':n,'scale':D,'a':[B]*n,'b':[-(2*r+2)]*n,
            'J':J,'low':0,'highs':[(B+2*a)*D for a in range(1,r+1)],
            'codes':[1<<i for i in range(n)],'f':list(f),'gates':gates}


def reset_machine(n: int, k: int | None = None) -> dict:
    """One-pulse reset of 1+k*(n-k+1) baseline-stable configurations."""
    require(type(n) is int and n >= 1, 'Need at least one switch')
    k = (n+1)//2 if k is None else k
    require(type(k) is int and 1 <= k <= n, 'Invalid target weight')
    target = (1<<k)-1
    codes = [target]
    codes += [target ^ (1<<j) for j in range(k)]
    codes += [(target ^ (1<<j)) | (1<<r) for j in range(k) for r in range(k,n)]
    W = 2*k+4
    a = [2 if i < k else 5 for i in range(n)]
    b = [v-W for v in a]
    J = [[2 if i >= k and j < k else 0 for j in range(n)] for i in range(n)]
    D = 8*(n+1)
    return {'kind':'affine','n':n,'scale':D,'a':a,'b':b,'J':J,'low':0,
            'highs':[3*D],'codes':codes,'f':[0]*len(codes),'target_weight':k}


def broom_machine(d: int) -> dict:
    """Optimal d-leaf -> intermediate -> fixed-point machine.

    The minimum is 1+ceil(2*sqrt(d)), implemented without floating-point sqrt.
    """
    require(type(d) is int and d >= 1, 'Need at least one leaf')
    n = 2
    while (n-1)**2//4 < d:
        n += 1
    k = (n-1)//2; errors = list(range(k+1,n)); e = len(errors)
    T = (1<<k)-1; p = k; R = T | (1<<p)
    leaves = [(T ^ (1<<j)) | (1<<r) for j in range(k) for r in errors][:d]
    W = max(2*k+4,2*e+4)
    a = [2 if i <= k else W+1-2*k for i in range(n)]
    b = [v-W for v in a]; J = [[0]*n for _ in range(n)]
    for r in errors:
        for j in range(k):
            J[r][j] = 2
        J[p][r] = 2
    D = 8*(n+1)
    return {'kind':'affine','n':n,'scale':D,'a':a,'b':b,'J':J,'low':0,
            'highs':[3*D],'codes':[R,T]+leaves,'f':[0,0]+[1]*d,'leaf_count':d}


def code_certificate(codes: list[int], f: list[int], n: int) -> dict:
    """Necessary and sufficient unary encoding conditions for arbitrary thresholds.

    Fixed points are normalized to no-switch states. This normalization is used
    for unrestricted threshold synthesis, not to assert fixed-degree optimality.
    """
    validate_map(f)
    require(type(n) is int and n >= 0, 'Invalid dimension')
    require(len(codes) == len(f) and len(set(codes)) == len(codes), 'Noninjective encoding')
    require(all(type(a) is int and 0 <= a < 1<<n for a in codes), 'Invalid bitmask')
    peak_target = {}; up = {}; code_set = set(codes)
    for i,j in enumerate(f):
        if i == j:
            continue
        A,T = codes[i],codes[j]; added,removed = T & ~A,A & ~T
        require(added.bit_count() == 1, 'A nontrivial transition must add one bit')
        require(removed.bit_count() <= 1, 'Too many removals')
        P = A | T
        if removed:
            require(P not in code_set, 'A descending peak cannot be a baseline code state')
        else:
            require(f[j] == j, 'Addition-only transitions must enter a fixed point')
        require(P not in peak_target or peak_target[P] == T,
                'A peak has incompatible required successors')
        peak_target[P] = T
        up[A] = added.bit_length()-1
    return {'up':{str(a):i for a,i in up.items()},
            'peak_target':{str(p):t for p,t in peak_target.items()}}


def table_compile(codes: list[int], f: list[int], n: int) -> dict:
    """Compile an admissible encoding into positive-span, band-separated tables.

    These tables need not be monotone outside the code trajectories. Global
    avalanche-freedom is not claimed for this constructor.
    """
    cert = code_certificate(codes,f,n)
    down = {p:(int(p)^t).bit_length()-1 for p,t in cert['peak_target'].items() if int(p)!=t}
    D = 8*(n+1)
    return {'kind':'table','n':n,'scale':D,'low':0,'highs':[3*D],
            'codes':list(codes),'f':list(f),'up':cert['up'],'down':down}


def layer_compile(codes: list[int], f: list[int], n: int,
                  saturating: bool = True, global_bands: bool = True) -> dict:
    """Compile every admissible constant-weight unary map, including merging.

    Polynomial shifts have degree k and nonnegative monomial coefficients.
    Saturated shifts are monotone in {0,2,4}, but their multilinear degree can
    be n-1. Saturation maintains constant field/span and global band separation.
    Unsaturated B=4 is also orbit-correct, but need not separate global bands.
    """
    cert = code_certificate(codes,f,n); k = codes[0].bit_count()
    require(1 <= k < n and all(a.bit_count()==k for a in codes), 'Not one interior layer')
    zeros = [set() for _ in range(n)]; fours = [set() for _ in range(n)]
    for a,i in cert['up'].items():
        zeros[i].add(int(a))
    for p,t in cert['peak_target'].items():
        r = (int(p)^t).bit_length()-1
        fours[r].add(t)
    require(all(not (zeros[i]&fours[i]) for i in range(n)), 'Conflicting edge labels')
    R = max(2*comb(n-1,k)-2*len(zeros[i])+2*len(fours[i]) for i in range(n))
    B = 4 if saturating or not global_bands else max(4,R)
    D = 8*(n+1)
    return {'kind':'saturating' if saturating else 'polynomial','n':n,'k':k,'scale':D,
            'low':0,'highs':[(B+1)*D],'a':[B]*n,'b':[-2]*n,
            'zeros':[sorted(x) for x in zeros],'fours':[sorted(x) for x in fours],
            'codes':list(codes),'f':list(f),'max_row_sum':R,
            'global_band_guarantee':bool(saturating or global_bands)}


def threshold(m: dict, i: int, state: int, up: bool) -> int:
    """Integer-scaled threshold; the element's own bit is always omitted."""
    D = m['scale']; env = state & ~(1<<i); kind = m['kind']
    if kind == 'affine':
        shift = sum(c for j,c in enumerate(m['J'][i]) if env>>j&1)
        v = (m['a'] if up else m['b'])[i]+shift
    elif kind in ('polynomial','saturating'):
        count = comb(env.bit_count(),m['k']) if env.bit_count() >= m['k'] else 0
        nz = sum(env & a == a for a in m['zeros'][i])
        nf = sum(env & a == a for a in m['fours'][i])
        shift = 2*count-2*nz+2*nf if kind=='polynomial' else (4 if nf else (2 if count>nz else 0))
        v = (m['a'] if up else m['b'])[i]+shift
    elif kind == 'table':
        if up:
            v = 2 if m['up'].get(str(env)) == i else 4
        else:
            v = 1 if m['down'].get(str(env | 1<<i)) == i else -2
    elif kind == 'raw':
        return m['plus' if up else 'minus'][i][env]
    else:
        raise ValueError('Unknown model kind')
    return D*v+i+1


def pulse(m: dict, initial: int, symbol: int = 0) -> dict:
    """Event-driven simulation independent of requested successor/event paths."""
    n = m['n']; L = m['low']; H = m['highs'][symbol]
    require(L < H, 'Invalid pulse endpoints')
    state = initial; events = []; slacks = []
    def stable(h):
        for i in range(n):
            gap = h-threshold(m,i,state,False) if state>>i&1 else threshold(m,i,state,True)-h
            require(gap > 0, f'Unstable state {state} at field {h}, bit {i}, slack {gap}')
            slacks.append(gap)
    stable(L)
    for rising,endpoint in ((True,H),(False,L)):
        flips = 0
        while True:
            cand = [(threshold(m,i,state,rising),i) for i in range(n)
                    if bool(state>>i&1) != rising]
            if not cand:
                break
            value,bit = min(cand) if rising else max(cand)
            if rising and value>endpoint or not rising and value<endpoint:
                break
            require(value != endpoint, 'A threshold coincides with a pulse endpoint')
            require(flips == 0, 'More than one flip on a half-pulse')
            for other,j in cand:
                if j != bit:
                    gap = other-value if rising else value-other
                    require(gap > 0, 'Nonunique switching winner')
                    slacks.append(gap)
            before = state; state ^= 1<<bit
            events.append({'up':rising,'bit':bit,'field_scaled':value,'before':before,'after':state})
            slacks.append(abs(endpoint-value)); stable(value); flips += 1
        stable(endpoint)
    return {'initial':initial,'final':state,'events':events,
            'min_slack_scaled':min(slacks,default=H-L)}


def check_machine(m: dict) -> dict:
    trials = 0; hist = [0,0,0]; minimum = None
    for a in range(len(m['highs'])):
        for i,state in enumerate(m['codes']):
            result = pulse(m,state,a); j = m['f'][i]
            if 'gates' in m and a+1 < m['gates'][i]:
                j = i
            require(result['final'] == m['codes'][j], 'Wrong target configuration')
            trials += 1; hist[len(result['events'])] += 1
            minimum = result['min_slack_scaled'] if minimum is None else min(minimum,result['min_slack_scaled'])
    return {'trials':trials,'flip_count_histogram':hist,
            'minimum_slack_numerator':minimum,'scale':m['scale']}


def cycle_codes(q: int) -> tuple[int,list[int]]:
    """Search-free constant-weight construction for every period q>=3.

    Use a reflected Gray-code ladder, dual-rail encoding, and for odd lengths
    insert one non-dual-rail state using an unused coordinate at a ladder end.
    """
    require(type(q) is int and q >= 3, 'Nontrivial periods start at 3; 2 is forbidden')
    if q in (3,5):
        return q,[1<<i for i in range(q)]
    even = q if q%2==0 else q-1
    t = even//2; r = (t-1).bit_length()+1
    gray = [j ^ (j>>1) for j in range(t)]
    words = gray + [v | 1<<(r-1) for v in reversed(gray)]
    codes = [sum(1<<(2*i+((v>>i)&1)) for i in range(r)) for v in words]
    if q%2:
        require(r >= 3, 'Odd insertion needs an unused coordinate')
        # Remove the occupied last-coordinate rail; add the unused second rail
        # of coordinate 1. Its other rail remains present, so the weight stays r.
        codes.append((codes[-1] & ~(3<<(2*(r-1)))) | (1<<3))
    return 2*r,codes


def cycle_model(q: int, saturating: bool = True, global_bands: bool = True) -> dict:
    n,codes = cycle_codes(q)
    return layer_compile(codes,list(range(1,q))+[0],n,saturating,global_bands)


def amplitude_certificate(table: list[list[int]]) -> dict:
    """Classify columns ordered by increasing positive pulse height."""
    require(bool(table) and bool(table[0]), 'Empty transition table')
    n = len(table); r = len(table[0]); f = []; gates = []
    for i,row in enumerate(table):
        require(len(row)==r and all(type(j) is int and 0<=j<n for j in row),'Invalid row')
        nonself = {j for j in row if j!=i}
        require(len(nonself)<=1,'A state has two different nonself destinations')
        f.append(next(iter(nonself),i))
        active = [a+1 for a,j in enumerate(row) if j!=i]
        gate = min(active) if active else 1
        require(not active or active==list(range(gate,r+1)),'Activation is not an upper tail')
        gates.append(gate)
    require(not has_two_cycle(f),'Highest-amplitude map has a two-cycle')
    return {'f':f,'gates':gates,'alphabet_size':r}


def amplitude_compile(table: list[list[int]]) -> dict:
    return one_hot(**amplitude_certificate(table))
