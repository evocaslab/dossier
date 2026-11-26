# The root justfile only imports modules: one module per area in just/<module>.just.
# `just` lists every recipe with its one-line description.

set positional-arguments
set quiet

import 'just/quality.just'

# List all recipes
[private]
default:
    just --list --unsorted --justfile {{ justfile() }}
