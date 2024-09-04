# PDF Search Tool

This Python program searches for a specific word in all PDF files within a specified folder and its subfolders. 
It provides the number of occurrences of the word in each document, extracts the line containing the word as well as the lines before and after it, and saves these results to a text file.

## Features

- Search for a specific word in all PDF files in a folder (including subfolders).
- Display the number of occurrences of the word in each document.
- Extract the line with the searched word and the lines before and after it.
- Save all results to a text file.
- Display results in the console as well.

## Requirements

- Python 3.x
- Dependencies: `PyPDF2`

Install the dependencies using the following command:

```bash
pip install PyPDF2


Usage
Clone this repository or download the code:

bash
Code kopieren
git clone https://github.com/your-username/pdf-search-tool.git
Navigate to the project directory:

bash
Code kopieren
cd pdf-search-tool
Edit the Python code to set the folder path and the word you want to search for:

folder_to_search: The path to the folder containing the PDF files to search.
word_to_search: The word to search for in the text.
output_file: The path to the text file where the results will be saved.
Run the script:

bash
Code kopieren
python pdf_search_tool.py
The results will be displayed in the console and saved in the specified text file.

Example
If you're searching for the word "example," the console output might look like this:

arduino
Code kopieren
File: document1.pdf
The word 'example' was found 3 times.

Occurrence 1: Page 2, Line 5
Previous Line: This is the line before the searched word.
Line with the searched word: This is an example sentence.
Next Line: This line follows the searched word.

...
The text file will store the same format to keep a record of the found results.

Customization
You can adjust the number of characters or lines displayed before and after the searched word in the code by modifying the appropriate section in the script.
Additional customizations, such as filtering file types or limiting the search to specific folders, can also be made by adjusting the script.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

markdown
Code kopieren

### Explanation of Sections:

1. **Title and Introduction**: Provides a short description of what the tool does.
2. **Features**: Lists the core features of the program.
3. **Requirements**: Specifies Python version and necessary dependencies.
4. **Usage**: Provides step-by-step instructions on how to run the program, including cloning the repository, modifying the script for folder and word input, and running the program.
5. **Example**: Gives an example of what the output will look like, both in the console and in the saved text file.
6. **Customization**: Suggests possible adjustments that users can make to the script.
7. **License**: Specifies the license under which the project is released, linking to the license file for details.

This `README.md` file is ready for use on GitHub and provides all necessary information for someone who wants to use or contribute to the project.
