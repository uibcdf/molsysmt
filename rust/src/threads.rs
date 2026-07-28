use pyo3::prelude::*;
use rayon::{ThreadPool, ThreadPoolBuilder};
use std::collections::HashMap;
use std::sync::{Arc, Mutex, OnceLock};

static POOLS: OnceLock<Mutex<HashMap<usize, Arc<ThreadPool>>>> = OnceLock::new();

fn pool(num_threads: usize) -> Arc<ThreadPool> {
    let pools = POOLS.get_or_init(|| Mutex::new(HashMap::new()));
    let mut pools = pools
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner());
    Arc::clone(pools.entry(num_threads).or_insert_with(|| {
        Arc::new(
            ThreadPoolBuilder::new()
                .num_threads(num_threads)
                .thread_name(move |index| format!("molsysmt-rayon-{num_threads}-{index}"))
                .build()
                .expect("MolSysMT could not create the requested Rayon thread pool"),
        )
    }))
}

pub fn install<OP, R>(num_threads: usize, operation: OP) -> R
where
    OP: FnOnce() -> R + Send,
    R: Send,
{
    pool(num_threads).install(operation)
}

#[pyfunction]
fn get_available_num_threads() -> usize {
    std::thread::available_parallelism()
        .map(|value| value.get())
        .unwrap_or(1)
}

#[pyfunction]
fn probe_num_threads(num_threads: usize) -> usize {
    install(num_threads, rayon::current_num_threads)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_available_num_threads, m)?)?;
    m.add_function(wrap_pyfunction!(probe_num_threads, m)?)?;
    Ok(())
}
