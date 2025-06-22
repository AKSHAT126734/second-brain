{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel

    pkgs.python311Packages.flask
    pkgs.python311Packages.requests
    pkgs.python311Packages.python_dotenv
    pkgs.python311Packages.dateparser
  ];
}
# force rebuild
