# Offline sandbox (orphan branch)

Built 2026-11-22T16:56:06Z from commit `2b2127d` for platform `linux-64`.
`pixi.lock` sha256 `1e6feedb5f9c13c5902011a4d1050b118c177861f77473568d9b473929bd0951`.

The verified self-bootstrap binary is stored at `.pixi-sandbox/tools/linux-64/pixi-sandbox`. The branch root intentionally contains documentation only.

| env | platform | packed | unpacked | files |
| --- | --- | ---: | ---: | ---: |
| `default` | linux-64 | 181.5 MiB | 651.2 MiB | 93 |


## Restore on the disconnected machine

```bash
./.pixi-sandbox/tools/linux-64/pixi-sandbox doctor --branch-location . --verify
./.pixi-sandbox/tools/linux-64/pixi-sandbox restore --branch-location . --output-path <project> --force
# then, from <project> with no network, use pixi as the sole entrypoint:
pixi install --frozen --offline
pixi run --frozen -- cargo build --offline
```

Every manifest blob is verified before it is written into the working tree.
