import polars as pl
from polars_bio.polars_bio import py_run_and_register_base_quality, py_read_sql
# from polars_bio.polars_bio import py_base_quality

# def base_quality(
#     input: pl.DataFrame,
#     streaming: bool = True,
#     target_partitions: int = None
# ) -> pl.DataFrame:
#     """
#     Calculate base sequence quality metrics from FASTQ data.
#     Parameters
#     ----------
#     input : pl.DataFrame
#         DataFrame with 'position' and 'quality' columns.
#     streaming : bool
#         Enable out-of-core processing if True.
#     target_partitions : int, optional
#         Level of parallelism for processing.
#     Returns
#     -------
#     pl.DataFrame
#         DataFrame with columns:
#         - position: u32
#         - average: f64
#         - q1: f64
#         - median: f64
#         - q3: f64
#         - min: f64
#         - max: f64
#         - warning_status: str
#     """
#     return py_base_quality(input, streaming, target_partitions)


def get_sequence_quality_stats(source_table):
    """
    Process sequence quality data from a source table and return statistics for each position.

    Parameters
    ----------
    source_table : str
        The name of the source table containing the raw data.

    Returns
    -------
    DataFrame
        A DataFrame with statistics (average, min, max, q1, median, q3) for each position.
    """
    print(source_table)
    # 1. Run your processing and register the result
    py_run_and_register_base_quality(source_table)

    # 2. Query the statistics
    df = py_read_sql("""
        SELECT
            position,
            AVG(score) AS average,
            MIN(score) AS min,
            MAX(score) AS max,
            approx_percentile_cont(score, 0.25) AS q1,
            approx_percentile_cont(score, 0.5) AS median,
            approx_percentile_cont(score, 0.75) AS q3
        FROM sequence_quality_result
        GROUP BY position
    """)

    return df
