import requests
from cat.mad_hatter.decorators import hook
from pydantic import BaseModel
from cat.experimental.form import CatForm,form
from cat.log import log

class FileUpload(BaseModel): #
    start_folder: str
    subfolders: bool
    files_extension: str

@form
class FileUploadForm(CatForm): 
    description = "Caricamento Documenti di Testo nel RAG" 
    model_class = FileUpload 
    start_examples = [
        "Aggiungi dei documenti al RAG",
        "Carica documenti nel sistema RAG",
        "Inserisci nuovi documenti nella knowledge base",
        "Aggiorna il RAG con nuovi file",
        "Carica file nel database di conoscenza",
        "Importa documenti nel sistema",
        "Aggiungi contenuti al retrieval system",
        "Carica nuovi testi nel RAG",
        "Aggiorna la base di conoscenza con nuovi documenti",
        "Inserisci file nel sistema di recupero",
        "Voglio aggiungere dei documenti",
        "Ho bisogno di caricare dei file",
        "Devo aggiornare la knowledge base",
    ]

    stop_examples = [
        "Annulla caricamento documenti",
        "Interrompi l'aggiunta al RAG",
        "Non voglio più caricare file",
        "Ferma l'importazione dei documenti",
        "Annulla l'operazione di caricamento"
    ]

    ask_confirm = True        

    def submit(self, form_data):
        import os
        from pathlib import Path
        from datetime import date

        # get data from form
        start_folder = form_data["start_folder"]
        subfolders = form_data["subfolders"]
        files_extension = form_data["files_extension"].lstrip('.').lower()  

        plugin_path = Path(self.cat.mad_hatter.get_plugin().path)
        dir_path: Path = plugin_path / start_folder

        if not os.path.exists(dir_path):
            return {
                "output": f"Il percorso {dir_path} non esiste. Verifica che sia corretto o crealo prima di procedere."
            }      

        if subfolders:
            files = dir_path.rglob(f"*.{files_extension}")
        else:
            files = dir_path.glob(f"*.{files_extension}")

        uploaded_files = []
        failed_files = []
        
        tot_files = len(files)
        step = 0

        # extracting filenames already present
        records, _ = self.cat.memory.vectors.declarative.get_all_points()
        sources = {record.payload['metadata']['source'] for record in records}  

        for file in files:
            step+=1
            if not file.is_file():
                continue

            file_full_name = Path(start_folder) / file.relative_to(dir_path)
            file_name = os.path.basename(file_full_name)
            base_path = Path(start_folder)
            file_relative_full_name = file_full_name.relative_to(base_path)
            
            log.info(f"CFF - working on file {step}/{tot_files}: {file_full_name}")

            # skip the file if is already in the rabbit_hole
            if str(file_full_name) in sources:
                log.warnig(f"CFF - skipped file {step}/{tot_files}: {file_full_name} already present.")
                failed_files.append(str(file_full_name))
                self.cat.send_chat_message(f"skipped file {step}/{tot_files}{file_full_name} already present.")
                continue

            # otherwise it's imported
            log.info(f"CFF - importing file {step}/{tot_files}...: {file_full_name}")
            file_content = file.read_text()
            docs = self.cat.rabbit_hole.string_to_docs(self.cat, file_content, "testo")
            self.cat.rabbit_hole.store_documents(
                self.cat, docs, str(file_relative_full_name),
                metadata={
                    "automatic_search": {"file_name": str(file_relative_full_name)},
                    "title": str(file_name),
                    "date": date.today().strftime("%Y-%m-%d")
                })

            uploaded_files.append(str(file_full_name))
            self.cat.send_chat_message(f"CFF - file {step}/{tot_files}: {file_full_name} successfully imported.")

        return {
            "output": f"""
                file importati: {len(uploaded_files)}
                file scartati perché già presenti: {len(failed_files)}
            """
        }

