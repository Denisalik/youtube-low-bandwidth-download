use minify_html::{minify, Cfg};
use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("usage: {} <input.html> <output.html>", args[0]);
        process::exit(2);
    }

    let input = &args[1];
    let output = &args[2];

    let src = match fs::read(input) {
        Ok(bytes) => bytes,
        Err(e) => {
            eprintln!("failed to read {}: {}", input, e);
            process::exit(1);
        }
    };

    // Configure minification.
    // https://docs.rs/minify-html/latest/minify_html/struct.Cfg.html
    let mut cfg = Cfg::new();
    
    cfg.minify_css = true;
    cfg.minify_js = true;
    cfg.minify_doctype = true;
    
    cfg.keep_closing_tags = false;
    cfg.keep_html_and_head_opening_tags = false;
    cfg.keep_comments = false;
    cfg.keep_ssi_comments = false;
    
    cfg.allow_optimal_entities = true;
    cfg.allow_removing_spaces_between_attributes = true;
    cfg.keep_input_type_text_attr = false;
    cfg.remove_bangs=true;
    cfg.remove_processing_instructions=true;


    let out = minify(&src, &cfg);

    if let Err(e) = fs::write(output, &out) {
        eprintln!("failed to write {}: {}", output, e);
        process::exit(1);
    }

    eprintln!(
        "minified {} -> {} ({} bytes -> {} bytes)",
        input,
        output,
        src.len(),
        out.len()
    );
}