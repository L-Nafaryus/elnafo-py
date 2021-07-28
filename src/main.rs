#[macro_use] extern crate rocket;

use rocket_dyn_templates::{Template};
use rocket::fs::FileServer;

use std::collections::HashMap;

mod files;

#[get("/")]
fn home() -> Template {
    let context: HashMap<&str, &str> = [("title", "ELNAFO")].iter().cloned().collect();

    Template::render("index", &context)
}
 
#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![home])
        .mount("/files", routes![files::files])
        .mount("/static", FileServer::from("static"))
        .attach(Template::fairing())
}
