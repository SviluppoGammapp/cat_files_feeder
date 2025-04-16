
import requests
from cat.mad_hatter.decorators import hook
from pydantic import BaseModel
from cat.experimental.form import CatForm,form
from cat.log import log

# @hook  # default priority = 1
# def before_agent_starts(agent_input, cat):
#     log.error(f"sono io:{cat}")

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
    
    # def submit(self, form_data):
    #     import os
    #     from pathlib import Path
    #     from datetime import date
        
    #     start_folder = form_data["start_folder"]
    #     subfolders = form_data["subfolders"]
    #     files_extension = form_data["files_extension"]

    #     if files_extension.startswith('.'):
    #         files_extension = files_extension.replace(".", "")

    #     plugin_path = Path(self.cat.mad_hatter.get_plugin().path)
                
    #     dir_path: Path = plugin_path / start_folder

    #     # verifica l'esistenza di dir_path
    #     if not os.path.exists(dir_path):
    #         return {
    #             "output": f"Il percorso {dir_path} non esiste. Verifica che sia corretto o crealo prima di procedere."
    #         }

    #     uploaded_files = []
    #     failed_files = []
        
    #     if subfolders:
    #         files = dir_path.rglob(f"*.{files_extension}")
    #     else:
    #         files = dir_path.glob(f"*.{files_extension}")

    #     for file in files:
    #         if not file.is_file():
    #             continue
            
    #         file_content = file.read_text()
    #         filename = start_folder / file.relative_to(dir_path)

    #         records, _ = self.cat.memory.vectors.declarative.get_all_points()

    #         sources = [record.payload['metadata']['source'] for record in records]
            
    #         log.error(f"SOURCES: {len(sources)}")

    #         for source in sources:
    #             if (
    #                 source == str(filename)
    #             ):
    #                 failed_files.append(filename)
    #                 self.cat.send_chat_message(f"skip {filename} already present.")
    #                 continue

            
    #             docs = self.cat.rabbit_hole.string_to_docs(self.cat, file_content, "testo")
    #             self.cat.rabbit_hole.store_documents(self.cat, docs, filename, 
    #                                                 metadata={
    #                                                         "automatic_search": {"file_name": filename},
    #                                                         "title": filename,
    #                                                         "date": date.today().strftime("%Y-%m-%d")
    #                                                     })

    #             uploaded_files.append(filename)
    #             self.cat.send_chat_message(f"ok.. {filename} loaded.")

    #     return {
    #         "output": f"""
    #             file importati: {len(uploaded_files)}
    #             file scartati perché già presenti: {len(failed_files)}
    #         """
    #     }
    

    # def submit(self, form_data):
    #     import os
    #     from pathlib import Path
    #     from datetime import date

    #     # Estrai dati dal form
    #     start_folder = form_data["start_folder"]
    #     subfolders = form_data["subfolders"]
    #     files_extension = form_data["files_extension"].lstrip('.')  # rimuove il punto se presente

    #     # Costruzione del path assoluto alla cartella di lavoro
    #     plugin_path = Path(self.cat.mad_hatter.get_plugin().path)
    #     dir_path: Path = plugin_path / start_folder

    #     # Verifica che il percorso esista
    #     if not os.path.exists(dir_path):
    #         return {
    #             "output": f"Il percorso {dir_path} non esiste. Verifica che sia corretto o crealo prima di procedere."
    #         }

    #     # Preparazione delle variabili
    #     uploaded_files = []
    #     failed_files = []

    #     # Seleziona i file da leggere (ricorsivo o no)
    #     if subfolders:
    #         files = dir_path.rglob(f"*.{files_extension}")
    #     else:
    #         files = dir_path.glob(f"*.{files_extension}")

    #     # Recupera i nomi dei file già presenti
    #     records, _ = self.cat.memory.vectors.declarative.get_all_points()
    #     sources = {record.payload['metadata']['source'] for record in records}  # set per performance

    #     # Ciclo sui file trovati
    #     for file in files:
    #         if not file.is_file():
    #             continue

    #         log.error(f"FILE: {filename}")

    #         file_content = file.read_text()
    #         filename = start_folder / file.relative_to(dir_path)

    #         # Se il file è già stato importato, lo salta
    #         if str(filename) in sources:
    #             log.error(f"FILE: {filename} PRESENTE")
    #             failed_files.append(filename)
    #             self.cat.send_chat_message(f"skip {filename} already present.")
    #             continue

    #         # Altrimenti lo importa
    #         log.error(f"FILE: {filename} IMPORTAZIONE")
    #         docs = self.cat.rabbit_hole.string_to_docs(self.cat, file_content, "testo")
    #         self.cat.rabbit_hole.store_documents(
    #             self.cat, docs, filename,
    #             metadata={
    #                 "automatic_search": {"file_name": filename},
    #                 "title": filename,
    #                 "date": date.today().strftime("%Y-%m-%d")
    #             })

    #         uploaded_files.append(filename)
    #         self.cat.send_chat_message(f"ok.. {filename} loaded.")

    #     # Report finale
    #     return {
    #         "output": f"""
    #             file importati: {len(uploaded_files)}
    #             file scartati perché già presenti: {len(failed_files)}
    #         """
    #     }

    def submit(self, form_data):
        import os
        from pathlib import Path
        from datetime import date

        # Estrai dati dal form
        start_folder = form_data["start_folder"]
        subfolders = form_data["subfolders"]
        files_extension = form_data["files_extension"].lstrip('.').lower()  # rimuove il punto se presente

        # Costruzione del path assoluto alla cartella di lavoro
        plugin_path = Path(self.cat.mad_hatter.get_plugin().path)
        dir_path: Path = plugin_path / start_folder

        # Verifica che il percorso esista
        if not os.path.exists(dir_path):
            return {
                "output": f"Il percorso {dir_path} non esiste. Verifica che sia corretto o crealo prima di procedere."
            }

        # Preparazione delle variabili
        uploaded_files = []
        failed_files = []

        tot_files = len(files)
        step = 0

        # Seleziona i file da leggere (ricorsivo o no)
        if subfolders:
            files = dir_path.rglob(f"*.{files_extension}")
        else:
            files = dir_path.glob(f"*.{files_extension}")

        # Recupera i nomi dei file già presenti
        records, _ = self.cat.memory.vectors.declarative.get_all_points()
        sources = {record.payload['metadata']['source'] for record in records}  # set per performance

        # Ciclo sui file trovati
        for file in files:
            step+=1
            if not file.is_file():
                continue

            # Calcola il nome relativo del file
            file_full_name = Path(start_folder) / file.relative_to(dir_path)
            file_name = os.path.basename(file_full_name)
            base_path = Path(start_folder)
            file_relative_full_name = file_full_name.relative_to(base_path)
            
            log.info(f"CFF - working on file {step}/{tot_files}: {file_full_name}")

            # Se il file è già stato importato, lo salta
            if str(file_full_name) in sources:
                log.warnig(f"CFF - skipped file {step}/{tot_files}: {file_full_name} already present.")
                failed_files.append(str(file_full_name))
                self.cat.send_chat_message(f"skipped file {step}/{tot_files}{file_full_name} already present.")
                continue

            # Altrimenti lo importa
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

        # Report finale
        return {
            "output": f"""
                file importati: {len(uploaded_files)}
                file scartati perché già presenti: {len(failed_files)}
            """
        }

