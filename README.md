<div align="center">

# ✿ HAVEN
### *a cozy file sanctuary for your downloads & chaos*

![Python](https://img.shields.io/badge/Python-3.10%2B-ebbcba?style=for-the-badge&logo=python&logoColor=191724)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-9ccfd8?style=for-the-badge&logo=qt&logoColor=191724)
![Theme](https://img.shields.io/badge/Theme-Rosé%20Pine-c4a7e7?style=for-the-badge)

</div>

---

**Haven** is a lightweight, ultra-compact desktop organizer designed to turn cluttered directories like `Downloads` into clean, structured spaces. Built with Python and PyQt6 using the **Rosé Pine** color palette.

---

### ✧ Features

* **Smart Categorization** — Automatically sorts files into `Images`, `Documents`, `Archives`, `Videos`, `Audio`, `Applications`, and `Other`.
* **Screenshot Cleanup** — Detects messy screenshot filenames and renames them chronologically (`Screenshot_YYYY-MM-DD_HHMMSS`).
* **Duplicate Detection** — Uses MD5 hash comparison to isolate identical files into a `Duplicates` folder.
* **Temp & Empty Folder Purge** — Removes temporary download files (`.tmp`, `.crdownload`, `.part`) and cleans up leftover empty directories.
* **Cozy & Portable** — Compact 420x360 GUI with zero external image asset requirements (dynamically generated vector icon).

---

### 🛠️ Getting Started

#### Prerequisites

Ensure you have Python 3.10+ installed.

#### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/your-username/haven.git](https://github.com/your-username/haven.git)
   cd haven