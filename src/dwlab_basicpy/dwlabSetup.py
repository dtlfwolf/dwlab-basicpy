import subprocess

def get_deb_package_version(package_name):
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Version}", package_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return f"Package '{package_name}' is not installed."

