let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/7acbf73b4759c9b8891f8710a36a1e3a93021e33.tar.gz";
  pkgs = import nixpkgs {};
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.5.0";
  }) {
    inherit pkgs;
  };
in
  mach-nix.mkPythonShell {
    python = "python39";
    requirements = builtins.readFile ./requirements.txt;
  }

