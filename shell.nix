let 
  pkgs = import <nixos> {};
in pkgs.mkShell {
        buildInputs = [ 
        pkgs.python3
        pkgs.python3Packages.pip
        pkgs.python3Packages.pygame
  ];  
  shellHook = ''
        alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"
        export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.7/site-packages:$PYTHONPATH"
        unset SOURCE_DATE_EPOCH
  '';
}
