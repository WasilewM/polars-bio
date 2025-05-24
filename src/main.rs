use arrow::array::{StringArray, ArrayRef};
use arrow::datatypes::{Field, DataType, Schema};
use arrow::record_batch::RecordBatch;
use std::sync::Arc;

mod base_quality;
use base_quality::compute_base_quality;

fn main() {
    let qual_data = vec![
        Some("IIII".to_string()), // 40, 40, 40, 40 (Phred: 'I' = 40)
        Some("####".to_string()), // 2, 2, 2, 2 (Phred: '#' = 2)
        Some("BBBB".to_string()), // 33, 33, 33, 33 (Phred: 'B' = 33)
    ];

    let qual_array: ArrayRef = Arc::new(StringArray::from(qual_data));
    let schema = Arc::new(Schema::new(vec![
        Field::new("qual", DataType::Utf8, true),
    ]));
    let batch = RecordBatch::try_new(schema, vec![qual_array]).unwrap();

    let df = compute_base_quality(&batch);
    println!("{}", df);
}
