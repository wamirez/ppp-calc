# Purchasing Power Parity calculator 

Adjust a given amount in USD for a given country after the [Purchasing Power Parity (PPP)](https://en.wikipedia.org/wiki/Purchasing_power_parity) indicator using the Netherlands as reference. Corresponding ratios are computed from the amounts provided by the [Google Summer of Code Stipend Amounts Table](https://developers.google.com/open-source/gsoc/help/student-stipends) (CC-BY-4.0).

## Usage

Specify amount [USD] and country in order to get the adjusted amount for the given country:

```console
$ python ppp.py 500 Brazil
278
```

The year can be specified when needed defaulting to the latest year otherwise:

```console
$ python ppp.py 500 Brazil 2022
333
```

The year has to correspond to a `<year>.csv` table whose contents can be fetched by using the helper script `update.py`. This script takes a URL to the Google SoC Contributor Stipends or a snapshot of it from previous years (see e.g., the [Wayback Machine](https://web.archive.org/web) of the Internet Archive to get a snapshot.) Its contents can then be stored in the working directory as follows:

```console
$ python update.py https://web.archive.org/web/20220809160247/https://developers.google.com/open-source/gsoc/help/student-stipends >> 2022.csv
```

## Nix

A Nix derivation, `shell.nix`, has been added to ensure reproducibility across the board. For starters, install Nix following [these](https://nix.dev/tutorials/install-nix) instructions. Cd to the directory that contains the files from the ppp-calc repository and run the shell as follows:

```console
$ cd (...)/ppp-calc
$ nix-shell
```

`nix-shell`, picks up `shell.nix` automatically installing required packages and creating a custom Python environment. Lastly, make scripts executables by:

```console
$ chmod -x ppp.py update.py
```
