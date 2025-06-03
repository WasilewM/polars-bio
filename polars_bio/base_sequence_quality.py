import polars_bio as pb
from polars_bio.polars_bio import py_run_and_register_base_quality

from .context import ctx


def base_sequence_quality(table: str):
    py_run_and_register_base_quality(ctx, table)
    pb_df = pb.sql("""
    SELECT
        position,
        AVG(score) AS average,
        approx_percentile_cont(score, 0.25) - 1.5 * (approx_percentile_cont(score, 0.75) - approx_percentile_cont(score, 0.25)) AS lower,
        approx_percentile_cont(score, 0.5) AS median,
        approx_percentile_cont(score, 0.25) AS q1,
        approx_percentile_cont(score, 0.75) AS q3,
        approx_percentile_cont(score, 0.75) + 1.5 * (approx_percentile_cont(score, 0.75) - approx_percentile_cont(score, 0.25)) AS upper
    FROM sequence_quality_result
    GROUP BY position
    """).collect()
    df = pb_df.to_pandas().set_index("position")
    return df
