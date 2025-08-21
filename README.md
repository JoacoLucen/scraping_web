<h1 align="center">📁 Scraping News</h1>

## 📑 Table of Contents
- [About the Project](#-about-the-project)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Developed By](#-developed-by)
- [Project Structure](#-project-structure)

--------------------------------------------------------------------
## 🌟 About the Project
"A program designed to scrape news channels in Argentina to obtain headlines and perform data analysis."

--------------------------------------------------------------------
## 🌳 Requirements

- **Python 3**
- **Code Editor**
- **Terminal/Console**

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

    python scraping.py

--------------------------------------------------------------------

## 👥 Developed By

- Lucentini Joaquin | 2025

--------------------------------------------------------------------
## 🌳 Project Structure

**What is the structure?**
- The scraping.py file contains the functions that will perform the scraping of news channels and get the headlines.
- The data_base.py file contains the functions that move the scraped data to the database. It also contains the queries for the database.

**Tree**

```bash
scraping_web/
├── data_base.py
│
├── scraping.py
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