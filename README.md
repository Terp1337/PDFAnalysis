# PDF Search Tool

This Python program searches for a specific word in all PDF files within a specified folder and subfolders. 
It provides the number of occurrences of the word in each document, extracts the line containing the word as well as the lines before and after it, and saves these results to a text file.

## Features

- Use GUI for enter search request
- Search for a specific word in all PDF files in a folder (including subfolders).
- Display the number of occurrences of the word in each document.
- Extract the line with the searched word and the lines before and after it.
- Save all results to a text file.
- Display results in the console as well.

## Requirements

- Python 3.x
- Dependencies: `PyPDF2`, `kivy`, `kivymd` 

Install the dependencies using the following command:

```
python -m pip install "kivy[full]" kivy_examples kivymd PyPDF

```

### Usage
1. Clone this repository or download the code:
```
git clone https://ithub.com/your-username/pdf-search-tool.git
```
2. Navigate to the project directory:

```
cd pdf-search-tool
```

3. Run the script:

```
python main.py
```

5. Use the app
   You can enter in the first row the word to search.
   You must enter in the secound row the folder with all PDF documents you will be scan.
   You can search all folders including subfolders.

   The results are displayed in the lower area.
   The search run is started with the `Search PDF` button. The `Save results` button creates a text file with all the results displayed.

### Example
If you're searching for the word "example," the  output might look like this:

```arduino
File: document1.pdf  |  The word 'example' was found 3 times.

Occurrence 1: Page 2, Line 5
Previous Line: This is the line before the searched word.
Line with the searched word: This is an example sentence.
Next Line: This line follows the searched word.

...
```
The text file will store the same format to keep a record of the found results.

### Customization
You can adjust the number of characters or lines displayed before and after the searched word in the code by modifying the appropriate section in the script.

Additional customizations, such as filtering file types or limiting the search to specific folders, can also be made by adjusting the script.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.
