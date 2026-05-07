# Multi-file pipeline operations

Some font build workflows require chutes that operate on two files simultaneously — a pattern the current `process(self, file)` API doesn't support natively. The canonical example is variable font production, where a CFF2 OTF and a variable TTF are both built from the same `.designspace` source and then need a table-swap step:

```
designspace → BuildMasterOtfs → BuildCff2Vf → Subroutinize ─┐
                                                               ├→ SwapTables → (OTF, TTF)
designspace → GenerateVariableTTF ─────────────────────────── ┘
```

This is a **fork/join** shape: two branches derive from the same input, process independently, then converge.

## Candidate APIs

### `Hellbox.fork`

Explicit symmetric branching. Both branches receive the same input file; the next chute in the outer pipeline receives a `FileGroup`:

```python
Hellbox.pipe(
    glob("*.designspace"),
    Hellbox.fork(
        [BuildMasterOtfs(), BuildCff2Vf(), Subroutinize()],  # → OTF
        [GenerateVariableTTF()],                              # → TTF
    ),
    SwapTables(),  # receives FileGroup, returns FileGroup
)
```

### `alongside`

Lighter-weight. Keeps a "primary" file flowing and attaches the result of a sub-pipeline as a secondary. Closer to the actual semantics when one file is the main artifact and another is derived in parallel:

```python
Hellbox.pipe(
    glob("*.designspace"),
    BuildMasterOtfs(),
    BuildCff2Vf(),
    alongside(GenerateVariableTTF()),  # produces (OTF, TTF) pair
    SwapTables(),
)
```

`fork` makes both branches explicit and equal. `alongside` treats one file as primary and the other as a companion — less symmetric but arguably clearer when there's a natural "main" artifact.

## Open questions

- Should `FileGroup` be ordered (tuple) or named (dict)?
- Can chutes downstream of a fork/join yield back to a flat stream, or do groups propagate?
- Does `alongside` need a way to specify which file in the pair flows as "primary" to the next chute if the next chute isn't group-aware?
