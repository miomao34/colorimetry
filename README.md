# colorimetry
A colorimetry app to determine color coordinates on CIE 1931 diagram and calculate correct coefficients for the spectrum mixing to get the spectrum of while light

---
### Prerequisites
* On Linux/Mac:
    - Install python 3 and git
        ```bash
        sudo apt install -y python3 git
        ```
    - Install tkinter lib
        ```bash
        sudo apt install -y python3-tk
        ```
* On Windows:
    - tbd
    <!-- - [Install Python 3](https://www.python.org/downloads/windows/) -->

---
### Compile and run
* On Linux/Mac:
    - Clone this repository
        ```bash
        git clone git@github.com:miomao34/colorimetry.git
        ```
    - Move into the repository folder and execute `setup` target of the makefile
        
        This step sets up the venv and downloads all the requirements except `tkinter` which was downloaded using `apt`
        ```bash
        cd colorimetry
        make setup
        ```
    - Put the data into this folder and change the `config.json` accordingly
    - Run the app
        ```bash
        make run
        ```

---

### Todo:
- [ ] Cleanup `main.py`, split UI into functions
- [ ] Add a more convenient config editor
- [ ] Add the while light coefficients calculation
- [ ] Calculate and plot the resulting white light spectrum
- [ ] Dump all the coordinates, coefficients and final spectrum into csv/txt/json
- [ ] Add 1 arbitrary point plotting
- [ ] Add various checks and failstate recoveries
- [x] Change `xyz` to `rgb` in config