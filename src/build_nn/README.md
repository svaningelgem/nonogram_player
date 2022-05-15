* take screenshots from the app
* save these into <root>/screenshots/levels/
* run `split_screenshots_in_numbers.py` script

  ==> This will extract the numbers into the <root>/screenshots/new_nr directory.
* **MANUAL ACTION**: see that all the numbers are in the correct directory (a lot might not be!)
* run `merge_into_nr_dir.py`

Run the added "Untitled.ipynb". This will generate several networks.

Copy the best h5 networks into the "nets" directory, don't change the name (or at least keep the last part "...-<accuracy>.hdf5")!

