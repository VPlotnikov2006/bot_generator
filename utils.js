export function* powerate(iter, k) {
    if (k == 1) {
        yield* iter.map(i => [i]);
    }
    else {
        for (let p of powerate(iter, k - 1)) {
            for (let i of iter) {
                yield [...p, i];
            }
        }
    }
}

export function* zip(...iter) {
    iter = iter.map(k => [...k])
    let n = Math.min(...iter.map(k => k.length));
    for (let i = 0; i < n; i++)
        yield iter.map(k => k[i]);
}


export function* uniformDistr(n, d, zero = false, one = false) {
    let k = Math.ceil(Math.pow(n, 1 / d));
    let r = []
    for (let i = 0; i < k; i++) {
        r.push((i + !zero) / (k + !zero + !one - 1))
    }
        
    yield* [...powerate(r, d)].slice(0, n);
}

export const clamp = (mn, val, mx) => {return Math.max(mn, Math.min(val, mx));}

export const dist = (x1, y1, x2, y2) => {
    return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
}