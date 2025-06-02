from .context import ctx
from polars_bio.polars_bio import (
    py_run_and_register_base_quality,
)


def base_sequence_quality(table: str):
    py_run_and_register_base_quality(ctx, table)
