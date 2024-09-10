#!/usr/bin/env python

import os, PyPDF2, re
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

# load external KV-file for GUI building
Builder.load_file('gui.kv')

def extract_text_from_pdf(pdf_file_path):
    """
    This function extracts the text page by page and saves each page as an element in a list.
    """
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text_by_page = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            text_by_page.append(text)
    return text_by_page

def find_word_context_in_page(text, word, page_num):
    """
    This function extracts the two lines before the search word,
    the line with the search word, and the two lines after it.
    """
    pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    matches = list(pattern.finditer(text))
    contexts = []

    lines = text.splitlines()
    for match in matches:
        start_index = match.start()

        # Find the line number
        line_num = 1
        char_count = 0
        for line in lines:
            char_count += len(line) + 1  # Adding 1 for the newline character
            if char_count >= start_index:
                break
            line_num += 1

        # Extract two previous, current, and two next lines
        previous_lines = lines[line_num - 3] if line_num > 2 else ""
        previous_line = lines[line_num - 2] if line_num > 1 else ""
        current_line = lines[line_num - 1]
        next_line = lines[line_num] if line_num < len(lines) else ""
        next_next_line = lines[line_num + 1] if line_num + 1 < len(lines) else ""

        context = {
            "page": page_num + 1,
            "line_num": line_num,
            "previous_lines": previous_lines.strip(),
            "previous_line": previous_line.strip(),
            "current_line": current_line.strip(),
            "next_line": next_line.strip(),
            "next_next_line": next_next_line.strip()
        }

        contexts.append(context)

    return len(matches), contexts

def analyze_pdf_for_word(pdf_file_path, word):
    """
    This function analyzes every page of the PDF document for the searched word and combines the results.
    """
    text_by_page = extract_text_from_pdf(pdf_file_path)
    total_word_count = 0
    contexts = []

    for page_num, text in enumerate(text_by_page):
        word_count, page_contexts = find_word_context_in_page(text, word, page_num)
        total_word_count += word_count
        contexts.extend(page_contexts)

    return total_word_count, contexts

def search_pdfs_in_folder(folder_path, word):
    """
    This function continues to search through all PDF files in the specified folder.
    """
    results = []
    total_files_searched = 0
    total_words_counted = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                total_files_searched += 1
                pdf_file_path = os.path.join(root, file)
                word_count, contexts = analyze_pdf_for_word(pdf_file_path, word)
                words_in_file = count_words_in_pdf(pdf_file_path)
                total_words_counted += words_in_file
                if word_count > 0:
                    results.append((file, word_count, contexts))

    return results, total_files_searched, total_words_counted

def save_results_to_textfile(results, word, output_file, total_files_searched, total_words_counted):
    """
    This function saves the results in a text file.
    It writes the file name, the number of occurrences,
    the page and the three relevant lines (previous line,
    line with search word, next line) to the file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Durchsuchte Dateien: {total_files_searched}\n")
        f.write(f"Gesamtanzahl der Wörter: {total_words_counted}\n\n")
        for result in results:
            pdf_file_name, word_count, contexts = result
            f.write(f"Datei: {pdf_file_name}\n")
            f.write(f"Das Wort '{word}' wurde {word_count} mal gefunden.\n")
            for context in contexts:
                f.write(f"\nSeite {context['page']}, Zeile {context['line_num']}:\n")
                if context['previous_line']:
                    f.write(f"1te Zeile: {context['previous_line']}\n")
                f.write(f"Suchwort : {context['current_line']}\n")
                if context['next_line']:
                    f.write(f"3te Zeile: {context['next_line']}\n")
                f.write("\n")
            f.write("\n" + "=" * 80 + "\n\n")

def count_words_in_pdf(pdf_file_path):
    """
    This function counts all words in a PDF document.
    """
    text_by_page = extract_text_from_pdf(pdf_file_path)
    total_word_count = 0

    for text in text_by_page:
        words = re.findall(r'\b\w+\b', text)
        total_word_count += len(words)

    return total_word_count

class MainScreen(Screen):
    input_word = ObjectProperty(None)
    result_output = ObjectProperty(None)
    folder_path = ObjectProperty(None)

    def search(self):
        word = self.input_word.text
        folder = self.folder_path.text

        if word and folder:
            results, total_files_searched, total_words_counted = search_pdfs_in_folder(folder, word)
            self.display_results(results, word, total_files_searched, total_words_counted)
        else:
            self.result_output.text = "Bitte geben Sie ein Suchwort und einen Ordner an."

    def display_results(self, results, word, total_files_searched, total_words_counted):
        """
        This function display the results in the GUI,
        including the additional row information.
        """
        if not results:
            self.result_output.text = f"Das Wort '{word}' wurde in keinem der PDF-Dokumente gefunden."
            return

        output_text = f"Durchsuchte Dateien: {total_files_searched}\n"
        output_text += f"Gesamtanzahl der Wörter: {total_words_counted}\n\n"
        for result in results:
            pdf_file_name, word_count, contexts = result
            output_text += "-" * 160 + "\n"
            output_text += f"\nDatei: {pdf_file_name}    |   "
            output_text += f"Das Wort '{word}' wurde {word_count} mal gefunden.\n"
            for idx, context in enumerate(contexts):
                output_text += f"Vorkommen {idx + 1}: Seite {context['page']}, Zeile {context['line_num']}\n"
                if context['previous_lines']:
                    output_text += f"1te Zeile: {context['previous_lines']}\n"
                if context['previous_line']:
                    output_text += f"2te Zeile: {context['previous_line']}\n"
                output_text += f"Suchwort : {context['current_line']}\n"
                if context['next_line']:
                    output_text += f"4te Zeile: {context['next_line']}\n"
                if context['next_next_line']:
                    output_text += f"5te Zeile: {context['next_next_line']}\n"
                output_text += "\n"
        self.result_output.text = output_text

    def save_results(self):
        """
        This function store the results in a file,
        including the additional row information.
        """
        word = self.input_word.text
        folder = self.folder_path.text
        if word and folder:
            results, total_files_searched, total_words_counted = search_pdfs_in_folder(folder, word)
            output_file = os.path.join(folder, 'ergebnisse.txt')
            save_results_to_textfile(results, word, output_file, total_files_searched, total_words_counted)
            self.result_output.text = f"Ergebnisse wurden in {output_file} gespeichert."
        else:
            self.result_output.text = "Bitte geben Sie ein Suchwort und einen Ordner an."

class PDFSearchAppMain(MDApp):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    PDFSearchAppMain().run()
