Sample code for using the SaintCoinach data mining tools to get new items and recipes from FFXIV. This is tailored specifically for getting *only* relevant items and recipes for craftable gear that would be used for week 1 progression. Intended to be used when the usual sites are not up to date due to a new patch.

## Requirements

This program relies on the SaintCoinach data mining tool to extract files from FFXIV's exd files. Get the latest release of SaintCoinach here: https://github.com/ufx/SaintCoinach/releases.

This program is written against Python 3.7. You'll need to install the following libraries via pip to get this to run:

```
pyyaml
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

These are made available in `requirements.txt`. You should be able to run the following command:

`python -m pip install -r requirements.txt`

Additionally, make a copy of `sample_config.yml`, rename it as `config.yml` and ensure the following two entries are defined with proper paths:

```yml
saint_coinach_install_location: Put SaintCoinach.Cmd.exe executable folder here!
ffxiv_install_location: Put FFXIV install folder here!
```

## Running the program

You should be able to run as follows:
```
python ./parse_game_data.py
```

Options for outputting data are included on the `--help` command.
