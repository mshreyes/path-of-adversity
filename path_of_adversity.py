"""
====================================================================
                        PATH OF ADVERSITY
         A Mechanistic Toxicology CLI Arcade Game for AOP-Wiki
====================================================================
"""

import sys
import os
import random
import xml.etree.ElementTree as ET

# ─── ANSI Terminal Palette ──────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def exit_game():
    clear_screen()
    print(f"{Color.GREEN}Path of Adversity session terminated. Goodbye!{Color.RESET}\n")
    sys.exit(0)

def prompt_continue_or_quit():
    """Prompt user to continue or quit at transition checkpoints."""
    ans = input(f"\n{Color.DIM}Press [ENTER] to continue, or [Q] to quit terminal > {Color.RESET}").strip().upper()
    if ans == "Q":
        exit_game()

def box_banner(title, subtitle=None, width=68, color=Color.CYAN):
    print(f"{color}╔{'═' * (width - 2)}╗{Color.RESET}")
    print(f"{color}║ {Color.BOLD}{title.center(width - 4)}{Color.RESET}{color} ║{Color.RESET}")
    if subtitle:
        print(f"{color}║ {Color.DIM}{subtitle.center(width - 4)}{Color.RESET}{color} ║{Color.RESET}")
    print(f"{color}╚{'═' * (width - 2)}╝{Color.RESET}")

def render_hud(mode_title, round_num, score, lives, streak):
    hearts = f"{Color.RED}{'♥ ' * lives}{'♡ ' * (3 - lives)}{Color.RESET}"
    multiplier = 1.0 + (streak * 0.25)
    hud_line = (
        f" {Color.CYAN}{mode_title}{Color.RESET} │ "
        f"ROUND: {Color.BOLD}{round_num:02d}{Color.RESET} │ "
        f"SCORE: {Color.GREEN}{score:04d} XP{Color.RESET} │ "
        f"LIVES: {hearts} │ "
        f"COMBO: {Color.YELLOW}{multiplier:.2f}x{Color.RESET}"
    )
    print(f"{Color.DIM}{'─' * 68}{Color.RESET}")
    print(hud_line)
    print(f"{Color.DIM}{'─' * 68}{Color.RESET}\n")

# ─── XML Parser ─────────────────────────────────────────────────────
def clean_tag(tag):
    return tag.split('}')[-1] if '}' in tag else tag

def load_aop_database(filepath="aop-wiki.xml"):
    """
    Extracts Chemicals, Key Events (KE), AOPs, and Key Event Relationships (KER)
    from the AOPWiki XML file.
    """
    data = {
        "chemicals": {},
        "key_events": {},
        "aops": {},
        "kers": {}
    }
    
    if not os.path.exists(filepath):
        return data

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for elem in root:
            tag = clean_tag(elem.tag)
            
            # 1. Chemicals
            if tag == "chemical":
                chem_id = elem.attrib.get("id")
                name, casrn, dsstox = None, "N/A", "N/A"
                synonyms = []
                for child in elem:
                    c_tag = clean_tag(child.tag)
                    if c_tag == "preferred-name" and child.text:
                        name = child.text.strip()
                    elif c_tag == "casrn" and child.text:
                        casrn = child.text.strip()
                    elif c_tag == "dsstox-id" and child.text:
                        dsstox = child.text.strip()
                    elif c_tag == "synonyms":
                        for s in child:
                            if s.text:
                                synonyms.append(s.text.strip())
                if name:
                    data["chemicals"][chem_id] = {
                        "name": name,
                        "casrn": casrn,
                        "dsstox": dsstox,
                        "synonyms": synonyms[:4]
                    }

            # 2. Key Events (KE)
            elif tag == "key-event":
                ke_id = elem.attrib.get("id")
                title, level = "Untitled Key Event", "Unspecified"
                for child in elem:
                    c_tag = clean_tag(child.tag)
                    if c_tag == "title" and child.text:
                        title = child.text.strip()
                    elif c_tag == "biological-organization" and child.text:
                        level = child.text.strip()
                if ke_id:
                    data["key_events"][ke_id] = {
                        "title": title,
                        "level": level
                    }

            # 3. Adverse Outcome Pathways (AOP)
            elif tag == "aop":
                aop_id = elem.attrib.get("id")
                title = "Untitled AOP"
                short_name = ""
                for child in elem:
                    c_tag = clean_tag(child.tag)
                    if c_tag == "title" and child.text:
                        title = child.text.strip()
                    elif c_tag == "short-name" and child.text:
                        short_name = child.text.strip()
                if aop_id:
                    data["aops"][aop_id] = {
                        "title": title,
                        "short_name": short_name
                    }

            # 4. Key Event Relationships (KER)
            elif tag == "key-event-relationship":
                ker_id = elem.attrib.get("id")
                upstream_id, downstream_id = "N/A", "N/A"
                adjacency = "non-adjacent"
                for child in elem:
                    c_tag = clean_tag(child.tag)
                    if c_tag == "title" and child.text:
                        title = child.text.strip()
                    elif c_tag == "upstream-id" and child.text:
                        upstream_id = child.text.strip()
                    elif c_tag == "downstream-id" and child.text:
                        downstream_id = child.text.strip()
                    elif c_tag == "relationship" and child.text:
                        adjacency = child.text.strip()
                if ker_id:
                    data["kers"][ker_id] = {
                        "upstream": upstream_id,
                        "downstream": downstream_id,
                        "adjacency": adjacency
                    }

    except Exception as e:
        print(f"{Color.RED}[!] XML parse error: {e}{Color.RESET}")

    return data

# ─── Curated Mechanistic Pathways ───────────────────────────────────
PATHWAYS = [
    {
        "chemical": "Rotenone",
        "category": "Pesticide / Mitochondrial Inhibitor",
        "mie": "Binding & inhibition of Mitochondrial Complex I (NADH:ubiquinone)",
        "ao": "Loss of Substantia Nigra Dopamine Neurons (Parkinsonian syndrome)",
        "chain": [
            ("Molecular", "Inhibition of Mitochondrial Complex I"),
            ("Cellular", "Electron leak & excess reactive oxygen species (ROS) formation"),
            ("Tissue", "Proteasome dysfunction & alpha-synuclein aggregation in substantia nigra"),
            ("Organism", "Progressive loss of dopamine neurons and severe locomotor deficit")
        ]
    },
    {
        "chemical": "Cadmium",
        "category": "Heavy Metal Environmental Contaminant",
        "mie": "High-affinity displacement of essential cations / -SH binding",
        "ao": "Proximal Tubular Epithelial Cell Death & Nephropathy",
        "chain": [
            ("Molecular", "Depletion of cellular glutathione (GSH) reserves"),
            ("Cellular", "Mitochondrial outer membrane permeabilization & calcium overload"),
            ("Tissue", "Proximal tubular epithelial cell apoptosis and necrosis"),
            ("Organism", "Loss of glomerular filtration and chronic renal failure")
        ]
    },
    {
        "chemical": "Lindane",
        "category": "Organochlorine Insecticide",
        "mie": "Non-competitive antagonism at the GABA-A receptor chloride pore",
        "ao": "Neuronal Hyperexcitability & Fatal Convulsions",
        "chain": [
            ("Molecular", "Blockade of GABA-gated chloride ion influx"),
            ("Cellular", "Loss of postsynaptic hyperpolarization (sustained excitation)"),
            ("Tissue", "Unchecked synchronous neuronal paroxysms across neocortex"),
            ("Organism", "Generalized tonic-clonic convulsions and CNS toxicity")
        ]
    },
    {
        "chemical": "Diclofenac sodium",
        "category": "Non-Steroidal Anti-Inflammatory Drug (NSAID)",
        "mie": "Enzyme catalytic inhibition of Cyclooxygenase (COX-1/COX-2)",
        "ao": "Severe Visceral Gout and Renal Collapse (Avian Mortality)",
        "chain": [
            ("Molecular", "Inhibition of COX-1 and COX-2 enzymatic activity"),
            ("Cellular", "Arteriole prostaglandin E2 synthesis suppression"),
            ("Tissue", "Renal medullary ischemia and severe uric acid accumulation"),
            ("Organism", "Visceral gout and lethal acute renal failure (Gyps vultures)")
        ]
    },
    {
        "chemical": "Simvastatin",
        "category": "HMG-CoA Reductase Inhibitor",
        "mie": "Competitive active-site blockade of HMG-CoA Reductase",
        "ao": "Acute Myocyte Necrosis & Lethal Rhabdomyolysis",
        "chain": [
            ("Molecular", "Active-site inhibition of HMG-CoA reductase"),
            ("Cellular", "Depletion of mevalonate, geranylgeranyl-PP, and Coenzyme Q10"),
            ("Tissue", "Myocyte ATP collapse and sarcoplasmic calcium leakage"),
            ("Organism", "Massive rhabdomyolysis with serum myoglobin-induced kidney damage")
        ]
    },
    {
        "chemical": "Benzo(a)pyrene",
        "category": "Polycyclic Aromatic Hydrocarbon (PAH)",
        "mie": "Metabolic activation to BPDE and covalent binding to DNA guanine residues",
        "ao": "Pulmonary / Hepatic Tumorigenesis",
        "chain": [
            ("Molecular", "Formation of stable (+)-anti-BPDE covalent DNA adducts"),
            ("Cellular", "Failure of nucleotide excision repair and replication stalling"),
            ("Tissue", "Clonal proliferation of mutated bronchial epithelial cells"),
            ("Organism", "Malignant pulmonary squamous cell carcinoma development")
        ]
    }
]

# ─── Game Modes ─────────────────────────────────────────────────────

def play_stressor_sleuth(chemicals):
    """GAME 1: Identify the chemical stressor matching an AOP mechanism."""
    score, lives, streak, round_num = 0, 3, 0, 1

    while lives > 0:
        clear_screen()
        render_hud("GAME 1: STRESSOR SLEUTH", round_num, score, lives, streak)
        
        target = random.choice(PATHWAYS)
        correct_chem = target["chemical"]

        matched = next((v for v in chemicals.values() if v["name"] == correct_chem), None)
        cas_hint = matched["casrn"] if matched else "In AOP-KB Registry"
        syn_hint = ", ".join(matched["synonyms"][:2]) if (matched and matched["synonyms"]) else "None indexed"

        print(f"{Color.BOLD}INVESTIGATIVE DOSSIER:{Color.RESET}")
        print(f"  ├─ {Color.CYAN}Molecular Initiating Event (MIE):{Color.RESET} {target['mie']}")
        print(f"  ├─ {Color.RED}Adverse Outcome (AO):{Color.RESET}             {target['ao']}")
        print(f"  ├─ {Color.MAGENTA}Class / Function:{Color.RESET}                 {target['category']}")
        print(f"  └─ {Color.DIM}Known Aliases / Synonyms:{Color.RESET}         {syn_hint}\n")

        pool = [c["name"] for c in chemicals.values() if c["name"] != correct_chem]
        if len(pool) < 3:
            pool += ["Acetaminophen", "Cisplatin", "Atrazine", "Warfarin"]
        options = random.sample(pool, 3) + [correct_chem]
        random.shuffle(options)

        letters = ["A", "B", "C", "D"]
        mapping = {}
        print(f"{Color.BOLD}Select the causative stressor chemical:{Color.RESET}")
        for l, opt in zip(letters, options):
            mapping[l] = opt
            print(f"  [{Color.BOLD}{l}{Color.RESET}] {opt}")

        guess = input(f"\n{Color.YELLOW}Enter suspect [A, B, C, D] or [Q] to quit to menu > {Color.RESET}").strip().upper()
        if guess == "Q":
            return

        if mapping.get(guess) == correct_chem:
            streak += 1
            pts = int(100 * (1.0 + (streak - 1) * 0.25))
            score += pts
            print(f"\n{Color.GREEN}{Color.BOLD}✔ CORRECT DOSSIER MATCH!{Color.RESET}")
            print(f"  Target confirmed as {Color.BOLD}{correct_chem}{Color.RESET} (CASRN: {cas_hint})")
            print(f"  {Color.GREEN}+{pts} XP added to record.{Color.RESET}")
        else:
            streak = 0
            lives -= 1
            correct_letter = [k for k, v in mapping.items() if v == correct_chem][0]
            print(f"\n{Color.RED}{Color.BOLD}✘ IDENTIFICATION MISMATCH.{Color.RESET}")
            print(f"  True causative agent: [{correct_letter}] {correct_chem}")

        round_num += 1
        if lives > 0:
            prompt_continue_or_quit()

    game_over_screen("STRESSOR SLEUTH", score, round_num - 1)


def play_cascade_scramble():
    """GAME 2: Assemble key events without biological levels shown until failed."""
    score, lives, streak, round_num = 0, 3, 0, 1

    while lives > 0:
        clear_screen()
        render_hud("GAME 2: CASCADE SCRAMBLE", round_num, score, lives, streak)

        target = random.choice(PATHWAYS)
        chain = target["chain"]
        shuffled = list(enumerate(chain))
        random.shuffle(shuffled)

        print(f"{Color.BOLD}CASCADE RESTORATION CHALLENGE:{Color.RESET}")
        print(f"Re-establish the biological chain of events for: {Color.CYAN}{target['chemical']}{Color.RESET}\n")

        letters = "ABCD"[:len(chain)]
        mapping = {}
        for l, (orig_idx, (_level, desc)) in zip(letters, shuffled):
            mapping[l] = orig_idx
            print(f"  [{Color.BOLD}{l}{Color.RESET}] {desc}")

        guess = input(f"\n{Color.CYAN}Enter causal order (e.g., {''.join(letters)}) or [Q] to quit to menu > {Color.RESET}").strip().upper().replace(" ", "")
        if guess == "Q":
            return

        if len(guess) != len(letters) or any(c not in mapping for c in guess):
            print(f"\n{Color.RED}[!] Invalid sequence length or character. Strike applied!{Color.RESET}")
            lives -= 1
            streak = 0
            print(f"\n{Color.YELLOW}Revealed Organizational Hierarchy:{Color.RESET}")
            for i, (lvl, desc) in enumerate(chain, 1):
                arrow = " ──► " if i < len(chain) else ""
                print(f"    {i}. {Color.MAGENTA}[{lvl.upper()}]{Color.RESET} {desc}{arrow}")
        else:
            ordered_indices = [mapping[c] for c in guess]
            if ordered_indices == list(range(len(chain))):
                streak += 1
                pts = int(120 * (1.0 + (streak - 1) * 0.25))
                score += pts
                print(f"\n{Color.GREEN}{Color.BOLD}✔ PATHWAY RESTORED!{Color.RESET}")
                print(f"  Biological sequence aligned flawlessly. {Color.GREEN}+{pts} XP{Color.RESET}")
            else:
                streak = 0
                lives -= 1
                print(f"\n{Color.RED}{Color.BOLD}✘ FAULTY CAUSAL PROGRESSION.{Color.RESET}")
                print(f"\n{Color.YELLOW}Biological Levels Revealed:{Color.RESET}")
                for i, (lvl, desc) in enumerate(chain, 1):
                    arrow = " ──► " if i < len(chain) else ""
                    print(f"    {i}. {Color.MAGENTA}[{lvl.upper()}]{Color.RESET} {desc}{arrow}")

        round_num += 1
        if lives > 0:
            prompt_continue_or_quit()

    game_over_screen("CASCADE SCRAMBLE", score, round_num - 1)


def game_over_screen(mode_name, score, rounds_played):
    clear_screen()
    box_banner("SIMULATION SESSION CONCLUDED", subtitle=f"Mode: {mode_name}", color=Color.YELLOW)
    print(f"\n  • Rounds Completed : {Color.BOLD}{rounds_played}{Color.RESET}")
    print(f"  • Final Score      : {Color.GREEN}{Color.BOLD}{score} XP{Color.RESET}")
    
    if score >= 500:
        rank = f"{Color.GREEN}Lead Mechanistic Toxicologist (Master of AOPs){Color.RESET}"
    elif score >= 200:
        rank = f"{Color.YELLOW}Regulatory Risk Assessor (Competent Practitioner){Color.RESET}"
    else:
        rank = f"{Color.RED}Laboratory Apprentice (Review OECD AOP Guidelines){Color.RESET}"
        
    print(f"  • Evaluated Rank   : {rank}\n")
    ans = input(f"{Color.DIM}Press [ENTER] for Main Menu, or [Q] to quit terminal > {Color.RESET}").strip().upper()
    if ans == "Q":
        exit_game()

# ─── Paginated XML Database Viewer ──────────────────────────────────

def paginate_records(title, records, formatter, page_size=10):
    """
    Renders records in a fully navigable page viewer with Next, Previous,
    direct Jump, and Quit options.
    """
    if not records:
        clear_screen()
        box_banner(title, color=Color.MAGENTA)
        print("\n  No records found in this category.")
        prompt_continue_or_quit()
        return

    total_records = len(records)
    total_pages = max(1, (total_records + page_size - 1) // page_size)
    current_page = 1

    while True:
        clear_screen()
        box_banner(title, subtitle=f"Page {current_page} of {total_pages} (Total: {total_records} records)", color=Color.MAGENTA)
        print()

        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_records)
        page_slice = records[start_idx:end_idx]

        for i, item in enumerate(page_slice, start=start_idx + 1):
            formatter(i, item)

        print(f"\n{Color.DIM}{'─' * 68}{Color.RESET}")
        nav_options = []
        if current_page < total_pages:
            nav_options.append(f"[{Color.BOLD}N{Color.RESET}]ext Page")
        if current_page > 1:
            nav_options.append(f"[{Color.BOLD}P{Color.RESET}]rev Page")
        nav_options.append(f"[{Color.BOLD}J{Color.RESET}]ump Page")
        nav_options.append(f"[{Color.BOLD}B{Color.RESET}]ack to Inspector")
        nav_options.append(f"[{Color.BOLD}Q{Color.RESET}]uit Game")
        print("  " + "  │  ".join(nav_options))
        print(f"{Color.DIM}{'─' * 68}{Color.RESET}")

        cmd = input(f"{Color.MAGENTA}Command > {Color.RESET}").strip().upper()

        if cmd == "N" and current_page < total_pages:
            current_page += 1
        elif cmd == "P" and current_page > 1:
            current_page -= 1
        elif cmd == "J":
            target = input(f"Enter page number (1-{total_pages}) > ").strip()
            if target.isdigit() and 1 <= int(target) <= total_pages:
                current_page = int(target)
        elif cmd == "B":
            break
        elif cmd == "Q":
            exit_game()

def view_xml_database(db):
    """Database inspection dashboard with pagination for all AOPWiki entities."""
    while True:
        clear_screen()
        box_banner("AOP-WIKI REGISTRY EXPLORER", subtitle="Comprehensive XML Knowledge Base", color=Color.MAGENTA)
        
        print(f"  Indexed Entity Breakdown:")
        print(f"   • Chemicals (Stressors)           : {Color.BOLD}{len(db['chemicals'])}{Color.RESET}")
        print(f"   • Key Events (KE)                 : {Color.BOLD}{len(db['key_events'])}{Color.RESET}")
        print(f"   • Adverse Outcome Pathways (AOP)  : {Color.BOLD}{len(db['aops'])}{Color.RESET}")
        print(f"   • Key Event Relationships (KER)   : {Color.BOLD}{len(db['kers'])}{Color.RESET}")
        print(f"\n{'─' * 68}")
        print(f"  [{Color.BOLD}1{Color.RESET}] Browse Chemical Stressors (Paginated)")
        print(f"  [{Color.BOLD}2{Color.RESET}] Browse Key Events (Paginated)")
        print(f"  [{Color.BOLD}3{Color.RESET}] Browse Adverse Outcome Pathways (Paginated)")
        print(f"  [{Color.BOLD}4{Color.RESET}] Browse Key Event Relationships (Paginated)")
        print(f"  [{Color.BOLD}B{Color.RESET}] Back to Main Menu")
        print(f"  [{Color.BOLD}Q{Color.RESET}] Quit Terminal")
        print(f"{'─' * 68}")

        sub = input(f"{Color.MAGENTA}Select category to inspect > {Color.RESET}").strip().upper()

        if sub == "1":
            chems = list(db["chemicals"].values())
            def fmt_chem(idx, c):
                syns = f" | Synonyms: {', '.join(c['synonyms'][:2])}" if c['synonyms'] else ""
                print(f"  {idx:03d}. {Color.BOLD}{c['name']}{Color.RESET} (CAS: {c['casrn']}){Color.DIM}{syns}{Color.RESET}")
            paginate_records("CHEMICAL STRESSORS", chems, fmt_chem)

        elif sub == "2":
            kes = list(db["key_events"].items())
            def fmt_ke(idx, item):
                ke_id, ke = item
                print(f"  {idx:03d}. [ID: {ke_id}] {Color.BOLD}{ke['title']}{Color.RESET}")
                print(f"       └─ Level: {Color.CYAN}{ke['level']}{Color.RESET}")
            paginate_records("KEY EVENTS (KE)", kes, fmt_ke)

        elif sub == "3":
            aops = list(db["aops"].items())
            def fmt_aop(idx, item):
                aop_id, aop = item
                short = f" ({aop['short_name']})" if aop['short_name'] else ""
                print(f"  {idx:03d}. [AOP #{aop_id}] {Color.BOLD}{aop['title']}{Color.RESET}{short}")
            paginate_records("ADVERSE OUTCOME PATHWAYS (AOP)", aops, fmt_aop)

        elif sub == "4":
            kers = list(db["kers"].items())
            def fmt_ker(idx, item):
                ker_id, ker = item
                print(f"  {idx:03d}. [KER #{ker_id}] KE_{ker['upstream']} ──► KE_{ker['downstream']} ({ker['adjacency']})")
            paginate_records("KEY EVENT RELATIONSHIPS (KER)", kers, fmt_ker)

        elif sub == "B":
            break
        elif sub == "Q":
            exit_game()

# ─── Terminal Menu System ───────────────────────────────────────────

def main():
    xml_path = sys.argv[1] if len(sys.argv) > 1 else "aop-wiki.xml"
    db = load_aop_database(xml_path)

    while True:
        clear_screen()
        box_banner("PATH OF ADVERSITY", subtitle="Mechanistic Toxicology Terminal Engine", color=Color.CYAN)
        
        status_line = (
            f" [Database Status: {Color.GREEN}{len(db['chemicals'])} Chems │ "
            f"{len(db['key_events'])} KEs │ {len(db['aops'])} AOPs │ {len(db['kers'])} KERs Loaded{Color.RESET}]"
            if any(db.values()) else
            f" [Database Status: {Color.YELLOW}Using Built-in AOP Curriculum{Color.RESET}]"
        )
        print(f"{status_line}\n")
        print(f"  {Color.BOLD}[1]{Color.RESET} Stressor Sleuth     ─ Identify chemicals by MIE and Adverse Outcome")
        print(f"  {Color.BOLD}[2]{Color.RESET} Cascade Scramble    ─ Reconstruct causal event chains (Levels hidden)")
        print(f"  {Color.BOLD}[3]{Color.RESET} View XML Database   ─ Inspect parsed Chemical, KE, AOP, and KER registry")
        print(f"  {Color.BOLD}[Q]{Color.RESET} Quit Terminal")
        print(f"\n{'─' * 68}")

        choice = input(f"{Color.CYAN}Select operation > {Color.RESET}").strip().upper()

        if choice == "1":
            play_stressor_sleuth(db["chemicals"])
        elif choice == "2":
            play_cascade_scramble()
        elif choice == "3":
            view_xml_database(db)
        elif choice == "Q":
            exit_game()

if __name__ == "__main__":
    main()