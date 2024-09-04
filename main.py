#!/usr/bin/env python

import PyPDF2
import re
import os


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
    This function extracts the line before the search word, 
    the line with the search word and the line after it.
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

        # Extract the previous, current, and next lines
        previous_line = lines[line_num - 2] if line_num > 1 else ""
        current_line = lines[line_num - 1]
        next_line = lines[line_num] if line_num < len(lines) else ""

        context = {
            "page": page_num + 1,
            "line_num": line_num,
            "previous_line": previous_line.strip(),
            "current_line": current_line.strip(),
            "next_line": next_line.strip()
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
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_file_path = os.path.join(root, file)
                word_count, contexts = analyze_pdf_for_word(pdf_file_path, word)
                if word_count > 0:
                    results.append((file, word_count, contexts))

    return results


def save_results_to_textfile(results, word, output_file):
    """
    This function saves the results in a text file. 
    It writes the file name, the number of occurrences, 
    the page and the three relevant lines (previous line, 
    line with search word, next line) to the file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
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


def display_results(results, word):
    """
    This function display the results in the console, 
    including the additional row information.
    """
    if not results:
        print(f"Das Wort '{word}' wurde in keinem der PDF-Dokumente gefunden.")
        return

    for result in results:
        pdf_file_name, word_count, contexts = result
        print(f"\nDatei: {pdf_file_name}")
        print(f"Das Wort '{word}' wurde {word_count} mal gefunden.\n")
        for idx, context in enumerate(contexts):
            print(f"Vorkommen {idx + 1}: Seite {context['page']}, Zeile {context['line_num']}")
            if context['previous_line']:
                print(f"1te Zeile: {context['previous_line']}")
            print(f"Suchwort : {context['current_line']}")
            if context['next_line']:
                print(f"3te Zeile: {context['next_line']}")
            print("\n")


# Beispielaufruf:
folder_to_search = 'C:\\MyFolder'  # Ersetze dies durch den Pfad zum Ordner
word_to_search = 'MyWord'  # Ersetze dies durch das zu suchende Wort
output_file = 'C:\\MyOutputFolder\\Output.txt'  # Pfad zur Ausgabedatei

results = search_pdfs_in_folder(folder_to_search, word_to_search)
display_results(results, word_to_search)
save_results_to_textfile(results, word_to_search, output_file)
