<img src="logo.png" width="150">

# 🐱 cat_files_feeder

**cat_files_feeder** is a tool designed to automate the ingestion of files into declarative memory using a prompt-based interface.

It works with a `@form` that requires three parameters:

- **start_folder**: specify the `files` folder or any subfolder within it. *(All files and folders to be ingested must be placed inside the `files` folder.)*
- **subfolders**: if `true`, the tool will also search inside subfolders.
- **files_extension**: specify a single file extension (e.g., `txt`, `java`, `md`).

> 📝 **All discovered files will be ingested as `text/plain`.**

---

## 🧠 Prompt Examples

- `importa i file .java dalla sola cartella files.`  
- `aggiungi i txt dalla cartella files e sottocartelle.`  
- `add all txt files from files and subfolders.`  
- `annulla` or `cancel` to cancel the import.

---

Enjoy!
