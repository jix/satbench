# SAT Benchmarking

Some early work in progress tooling for running benchmarks and keeping track of
the results when working on SAT solvers and related tools.

Written with only my personal use in mind. There is no documentation and no
stability guarantee. Nevertheless, feel free to use and adapt it for your own
needs, as long as you don't expect support from me.

This includes the `data` directory, so I can easily use the same git repository
to keep track of the tooling as well as the benchmarks and results over time.
This will allow me to later figure out how to reproduce old results even after
I changed the tooling in some incompatible way.

The repository doesn't include the corresponding `blobs` directory though,
which contains binary files and is multiple GB in size. This means not
everything in here will work with the existing `data` directory.

In any case, if you start using this yourself, I'd recommend maintaining your
own fork without trying to closely follow this repository.

# Commands

I recommend reading the source of any command before running it, there's no
other way to figure out how to use most of them.

* `setup/setup` setups a venv in `env`, compiles rust code in `tools` and links
  binaries into `env`. Required for any other command to work. Some code is in
  submodules.
* `scripts/start` starts the benchrunner daemon. Requires creating a `env.ini`
  before.
* `scripts/load_cnf` loads cnf files from a directory, decompresses them if
  required, normalizes and hashes them and finally compresses them with cnfpack
  if not already present.
