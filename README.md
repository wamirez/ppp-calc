# Purchasing power parity calculator 

Adjust a given amount for a given country after the [purchasing power parity (PPP)](https://en.wikipedia.org/wiki/Purchasing_power_parity) indicator using the Netherlands as reference. Corresponding ratios are computed from the amounts provided by the [Google Summer of Code Stipend Amounts Table](https://developers.google.com/open-source/gsoc/help/student-stipends) (CC-BY-4.0), and rounded to an integer.

## Usage

Specify amount and country in order to get the adjusted amount for the given country:

```console
$ python ppp.py 500 Brazil
278
```

Set a different reference country with `--reference`:

```console
$ python ppp.py 500 Brazil --reference Australia
227
```

The year can be specified when needed, defaulting to the current year:

```console
$ python ppp.py 500 Brazil 2022
333
```

## Purchasing power parity data

The year has to correspond to a `<year>.csv` table whose contents can be fetched by using the helper script `update.py`. This script takes a URL to the GSoC contributor stipends page, or a snapshot of it from previous years (see e.g., the [Wayback Machine](https://web.archive.org/web) of the Internet Archive to get a snapshot). Its contents can then be stored in the working directory as follows:

```console
$ python update.py https://web.archive.org/web/20220809160247/https://developers.google.com/open-source/gsoc/help/student-stipends >> 2022.csv
```

## Nix

A Nix derivation, `shell.nix`, has been added to ensure reproducibility across the board.

- [Install Nix](https://nix.dev/tutorials/install-nix)
- Clone this repository

  ```console
  git clone https://github.com/wamirez/ppp-calc
  ```

- Enter the Nix shell

  ```console
  $ cd ppp-calc
  $ nix-shell
  ```

`nix-shell` picks up `shell.nix` automatically installing required packages and creating a custom Python environment.
