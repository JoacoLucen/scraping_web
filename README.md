<h1 align="center">📁 Scraping News</h1>

## 📑 Table of Contents
- [About the Project](#-about-the-project)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Developed By](#-developed-by)
- [Project Structure](#-project-structure)

--------------------------------------------------------------------
## 🌟 About the Project
"A program to scrape news channels in Argentina, and obtain titles and store them in SQLite.
Then with this data, clean it and perform an analysis of it using the Streamlit library. Additionally, I added functionality to generate an automatic PDF file with the analysis performed"

--------------------------------------------------------------------
## 🌳 Requirements

- **Python 3**
- **Code Editor**
- **Terminal/Console**
- **Google Browser**

--------------------------------------------------------------------
## 🛠️ Installation

Follow these steps to set up the development environment:

1. **Clone the repository**:
   ```bash
   Clone with SSH
   git clone git@github.com:JoacoLucen/scraping_web.git
   Clone with HTTPS
   git clone [https://github.com/JoacoLucen/scraping_web.git](https://github.com/JoacoLucen/scraping_web.git)

2. **Enter the project folder**:

    cd scraping_web

3. **Create and activate the virtual environment**:
    **Windows**

    python -m venv venv  ----------  .\venv\Scripts\activate

    **Linux/Mac**

    python3 -m venv venv  ---------  source venv/bin/activate

4. **Install the requirements**:

    pip install -r requirements.txt

4. **Run the Program from the Terminal**: 

    cd src

    python scraping.py (If you want to do a scrapping)

    streamlit run app.py (If you want to view the Streamlit page and generate the PDF file, with the current data)


--------------------------------------------------------------------

## 👥 Developed By

- Lucentini Joaquin | 2025

--------------------------------------------------------------------
## 🌳 Project Structure

**What is the structure?**
- The src folder contains the files necessary for the program's functionality.
- The resource folder contains the folders necessary to store the images and the PDF file for analysis.
- The scraping.py file contains the functions that will perform the scraping of news channels and get the headlines.
- The data_base.py file contains the functions that move the scraped data to the database. It also contains the queries for the database.
- The clear_stats.py file contains all the functions to get the data from the database
- The app.py file contains the main structure for displaying the data

**Tree**

```bash
scraping_web/
├── resource/
│   ├── img/
│   └── pdf/
├── src/
│   ├── app.py
│   ├── clear_stats.py
│   ├── noticias.db
│   ├── pdf_create.py
│   ├── scraping.py
│   └── data_base.py
│ 
├── requirements.txt      
│ 
├── README.md
│ 
├── license.txt
│ 
└── .gitignore
```

--------------------------------------------------------------------
<details>
<summary>📝 MIT License</summary>

Copyright (c) [2025] [Lucentini Joaquin]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

</details>