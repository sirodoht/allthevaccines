with import <nixpkgs> {};
let
  my-python-packages = python-packages: [
    python-packages.pip
    python-packages.django
  ];
  my-python = python39.withPackages my-python-packages;
in
  pkgs.mkShell {
    buildInputs = [
      bashInteractive
      my-python
    ];
    shellHook = ''
      export PIP_PREFIX="$(pwd)/.pyenv/pip_packages"
      export PYTHONPATH="$(pwd)/.pyenv/pip_packages/lib/python3.9/site-packages:$PYTHONPATH"
      unset SOURCE_DATE_EPOCH
    '';
  }
