use std::collections::HashMap;
use std::rc::Rc;

use crate::{DependencyMap, Task, WorkingSet};
use pyo3::prelude::*;
use taskchampion::storage::{InMemoryStorage, SqliteStorage};
use taskchampion::{Replica as TCReplica, Uuid};

#[pyclass]
/// A replica represents an instance of a user's task data, providing an easy interface
/// for querying and modifying that data.
pub struct Replica(TCReplica);

unsafe impl Send for Replica {}
#[pymethods]
impl Replica {
    #[new]
    /// Instantiates the Replica
    ///
    /// Args:
    ///     path (str): path to the directory with the database
    ///     create_if_missing (bool): create the database if it does not exist
    /// Raises:
    ///     RuntimeError: if database does not exist, and create_if_missing is false
    pub fn new(path: String, create_if_missing: bool) -> anyhow::Result<Replica> {
        let storage = SqliteStorage::new(path, create_if_missing)?;

        Ok(Replica(TCReplica::new(Box::new(storage))))
    }

    #[staticmethod]
    pub fn new_inmemory() -> Self {
        let storage = InMemoryStorage::new();

        Replica(TCReplica::new(Box::new(storage)))
    }
    /// Create a new task
    /// The task must not already exist.

    /// Get a list of all uuids for tasks in the replica.
    pub fn all_task_uuids(&mut self) -> anyhow::Result<Vec<String>> {
        Ok(self
            .0
            .all_task_uuids()
            .map(|v| v.iter().map(|item| item.to_string()).collect())?)
    }

    /// Get a list of all tasks in the replica.
    pub fn all_tasks(&mut self) -> anyhow::Result<HashMap<String, Task>> {
        Ok(self
            .0
            .all_tasks()?
            .into_iter()
            .map(|(key, value)| (key.to_string(), Task(value)))
            .collect())
    }

    pub fn working_set(&mut self) -> anyhow::Result<WorkingSet> {
        Ok(self.0.working_set().map(|ws| WorkingSet(ws))?)
    }

    pub fn dependency_map(&mut self, force: bool) -> anyhow::Result<DependencyMap> {
        // TODO: kinda spaghetti here, it will do for now
        let s = self
            .0
            .dependency_map(force)
            .map(|rc| {
                // TODO: better error handling here
                Rc::into_inner(rc).unwrap()
            })
            .map(|dm| DependencyMap(dm))?;

        Ok(s)
    }

    pub fn get_task(&mut self, uuid: String) -> anyhow::Result<Option<Task>> {
        Ok(self
            .0
            .get_task(Uuid::parse_str(&uuid).unwrap())
            .map(|opt| opt.map(|t| Task(t)))?)
    }

    pub fn sync(&self, _avoid_snapshots: bool) {
        todo!()
    }

    pub fn rebuild_working_set(&mut self, renumber: bool) -> anyhow::Result<()> {
        Ok(self.0.rebuild_working_set(renumber)?)
    }
    pub fn num_local_operations(&mut self) -> anyhow::Result<usize> {
        Ok(self.0.num_local_operations()?)
    }

    pub fn num_undo_points(&mut self) -> anyhow::Result<usize> {
        Ok(self.0.num_local_operations()?)
    }
}
