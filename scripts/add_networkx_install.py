"""
Add installation cell for networkx at the beginning of notebook
"""

import json

def add_networkx_install_cell():
    """Add cell to install networkx if needed"""
    
    install_cell = {
        "cell_type": "code",
        "execution_count": None,
        "id": "install_networkx",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Install networkx if not already installed\n",
            "import subprocess\n",
            "import sys\n",
            "\n",
            "try:\n",
            "    import networkx as nx\n",
            "    print(\"NetworkX already installed, version:\", nx.__version__)\n",
            "except ImportError:\n",
            "    print(\"Installing NetworkX...\")\n",
            "    subprocess.check_call([sys.executable, \"-m\", \"pip\", \"install\", \"-q\", \"networkx\"])\n",
            "    import networkx as nx\n",
            "    print(\"NetworkX installed successfully, version:\", nx.__version__)"
        ]
    }
    
    return install_cell

def main():
    print("Loading project.ipynb...")
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Find the first library installation cell (after the title)
    insert_index = 1  # After first markdown cell
    
    # Check if networkx install cell already exists
    has_networkx_cell = False
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and 'source' in cell:
            source = ''.join(cell['source'])
            if 'import networkx' in source and 'subprocess' in source:
                has_networkx_cell = True
                break
    
    if has_networkx_cell:
        print("NetworkX installation cell already exists, skipping...")
    else:
        print("Adding NetworkX installation cell...")
        new_cell = add_networkx_install_cell()
        notebook['cells'].insert(insert_index, new_cell)
        
        print("Saving updated notebook...")
        with open('project.ipynb', 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        print("\n[OK] NetworkX installation cell added!")
    
    print("\nNext steps:")
    print("1. In Jupyter, click 'Kernel' -> 'Restart'")
    print("2. Run the new installation cell")
    print("3. Then run 'Run All' to execute all cells")

if __name__ == "__main__":
    main()
