use rocket_dyn_templates::Template;
use rocket::serde::Serialize;

use std::path::{Path, PathBuf};
use std::fs;
use std::time::SystemTime;
use std::collections::HashMap;

#[derive(Hash, Eq, PartialEq, Debug, Serialize)]
#[serde(crate = "rocket::serde")]
 struct FileInfo {
    name: PathBuf,
    isfile: bool,
    modified: SystemTime
 }

 impl FileInfo {
    fn new(name: PathBuf, isfile: bool, modified: SystemTime) -> FileInfo {
        FileInfo { 
            name: name, 
            isfile: isfile, 
            modified: modified 
        }
    }
 }

#[get("/")]
pub fn files() -> Template {
    let root = Path::new(concat!(env!("CARGO_MANIFEST_DIR"), "/public"));
    let mut filesinfo = HashMap::new();

    for entry in fs::read_dir(&root).unwrap() {
        let path = entry.unwrap().path();
        let attr = fs::metadata(&path).unwrap();

        filesinfo.insert(
            path.clone(),
            FileInfo::new(path.clone(), attr.is_file(), attr.modified().unwrap())
        );
    }

    Template::render("files", &filesinfo)
}
