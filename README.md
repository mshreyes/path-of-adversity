# Path of Adversity


`path-of-adversity` is an interactive terminal arcade game designed for toxicologists, computational biologists, regulatory scientists, and students. It parses official [AOP-Wiki](https://aopwiki.org/) XML knowledge base snapshots and turns them into mechanistic puzzle modes exploring Adverse Outcome Pathways (AOPs), Molecular Initiating Events (MIEs), Key Events (KEs), and Key Event Relationships (KERs).

---

## Features

* **Game 1: Stressor Sleuth**:
  * Receive an investigative dossier featuring a Molecular Initiating Event (MIE), Adverse Outcome (AO), compound category, and chemical synonyms.
  * Deduce the causative chemical stressor from a randomized multi-choice lineup.


* **Game 2: Cascade Scramble**:
  * Reconstruct randomized causal pathway cascades from initial molecular trigger down to organism/population-level effects.
  * **Mechanistic Challenge**: Biological organization levels (`[MOLECULAR]`, `[CELLULAR]`, `[TISSUE]`, `[ORGANISM]`) remain hidden during puzzle solving and are only unveiled as an educational debrief if a sequence fails.


* **Interactive XML Database Explorer**:
  * Full pagination viewer across all parsed database entities:
  * **Chemical Stressors** (Names, CASRN, DSSTox IDs, Synonyms)
  * **Key Events (KE)** (Titles, Organizational Levels)
  * **Adverse Outcome Pathways (AOP)** (Titles, Short Names)
  * **Key Event Relationships (KER)** (Upstream/Downstream links, Adjacency)
  * Navigate with `[N]`ext, `[P]`revious, `[J]`ump to page, or return with `[B]`ack.


* **Universal Exit (`[Q]`)**:
  * Quit to menu or cleanly exit the terminal session at any decision checkpoint, round prompt, or viewer screen.


* **Arcade Terminal Interface**:
  * ANSI color-coded layouts, live life counters (`♥♥♥`), dynamic combo multipliers, and post-session rank evaluations based on OECD AOP developer benchmarks.


* **Zero External Dependencies**:
  * Built exclusively on Python standard libraries (`xml.etree.ElementTree`, `random`, `sys`, `os`).



---

## Project Structure

```text
path-of-adversity/
├── README.md
├── LICENSE
├── aop-wiki.xml            # AOP-Wiki full XML data dump
└── path_of_adversity.py    # Game executable

```

---

## Getting Started

### Prerequisites

* Python 3.8 or higher.
* A terminal emulator supporting ANSI escape colors (e.g., Windows Terminal, iTerm2, macOS Terminal, Alacritty, GNOME Terminal).

### Installation

Clone the repository:

```bash
git clone [https://github.com/your-username/path-of-adversity.git](https://github.com/your-username/path-of-adversity.git)
cd path-of-adversity

```

Make the script executable:

```bash
chmod +x path_of_adversity.py

```

---

## Usage

### Running with Built-in Curriculum

If no external XML file is provided, the engine runs off its embedded canonical toxicology dataset:

```bash
python3 path_of_adversity.py

```

### Running with Official AOP-Wiki XML Data

1. Download the latest XML data snapshot from [AOP-Wiki Downloads](https://aopwiki.org/downloads).
2. Extract the archive to obtain `aop-wiki.xml`.
3. Place `aop-wiki.xml` in the project root directory, or specify its file path when running:

```bash
python3 path_of_adversity.py path/to/aop-wiki.xml

```

---

## Gameplay & Controls

### Main Navigation

* `[1]`: Launch **Stressor Sleuth**
* `[2]`: Launch **Cascade Scramble**
* `[3]`: Enter **AOP-Wiki Registry Explorer**
* `[Q]`: Quit application

### Pager Controls (Database Explorer)

* `[N]`: Next page
* `[P]`: Previous page
* `[J]`: Jump to a specific page number
* `[B]`: Back to registry menu
* `[Q]`: Quit application

---

## License

MIT

## Disclaimer

Google Gemini 3.8 Flash was used to tidy up the code and generate the README.md file.
