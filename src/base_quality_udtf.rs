use std::sync::Arc;
use datafusion::common::{plan_err, ScalarValue, Result};
use datafusion::catalog::TableProvider;
use datafusion::datasource::function::TableFunctionImpl;
use datafusion::datasource::memory::MemTable;
use arrow::datatypes::{DataType, Field, Schema};
use datafusion_expr::Expr;
use exon::ExonSession;

use crate::operation::do_base_sequence_quality_as_batches;

pub struct BaseSequenceQualityUdtf {
    ctx: ExonSession,
}

impl std::fmt::Debug for BaseSequenceQualityUdtf {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("BaseSequenceQualityUdtf")
            .finish()
    }
}

impl TableFunctionImpl for BaseSequenceQualityUdtf {
    fn call(&self, exprs: &[Expr]) -> Result<Arc<dyn TableProvider>> {
        // 1. Parse input arguments (e.g., table name)
        let Some(Expr::Literal(ScalarValue::Utf8(Some(table_name)))) = exprs.get(0) else {
            return plan_err!("First argument must be a string (table name)");
        };

        // 2. Run your processing logic (similar to do_base_sequence_quality)
        //    This is where you would use your existing logic to process the table.
        //    For this example, we'll assume you have a function that returns RecordBatches.
        //    In practice, you would need to adapt your logic to work here.
        let batches = tokio::runtime::Runtime::new()
            .unwrap()
            .block_on(do_base_sequence_quality_as_batches(&self.ctx, &table_name))?;


        let schema = Arc::new(Schema::new(vec![
            Field::new("position", DataType::Int64, false),
            Field::new("score", DataType::Float64, false),
        ]));

        let provider = MemTable::try_new(schema, vec![batches])?;
        Ok(Arc::new(provider))
    }
}
