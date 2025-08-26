from requests import get
from os import makedirs, execv
from shutil import rmtree
from subprocess import check_output


class ReleaseAPI:
    """
    a class to check for software updates and handle updates

    a new version is detected when there is a new release on the github releases page
    every release should have at least 1 asset, a script to install the new version
    which should be named <tag_name>.sh for example, v1.0.0.sh. a template for this script
    can be found in the resources directory of the repository named release_template.sh
    """

    REPO_URL = "https://api.github.com/repos/TB543/4RunnerDash/releases/latest"

    def __init__(self, shutdown):
        """
        creates the release manager

        @param callback: the shutdown callback to call before updating
        """

        # sets fields
        self.callback = shutdown
        self.current_release = check_output(["git", "describe", "--tags", "--abbrev=0"]).decode("utf-8").strip()
        
        # pulls the latest release from github
        try:
            self.new_release = get(
                ReleaseAPI.REPO_URL,
                timeout=5
            ).json()

        # returns the current release if there is no internet connection
        except Exception:
            self.new_release = None

    def update_available(self):
        """
        checks if a new version is available

        @return: True if a new version is available, False otherwise
        """

        return self.new_release and (self.new_release["tag_name"] != self.current_release)
        
    def update(self):
        """
        updates the software to the latest version
        """

        # downloads required files
        makedirs(f"../{self.new_release['tag_name']}", exist_ok=True)
        try:
            for asset in self.new_release["assets"]:
                with open(f"../{self.new_release['tag_name']}/{asset['name']}", "wb") as f:
                    f.write(get(
                        asset["browser_download_url"],
                        timeout=5
                    ).content)
        
        # removes new version if error occurs
        except Exception:
            rmtree(f"../{self.new_release['tag_name']}")

        # installs the new version
        self.callback()
        execv("/bin/bash", ["/bin/bash", f"../{self.new_release['tag_name']}/{self.new_release['tag_name']}.sh", self.new_release['tag_name']])


print(ReleaseAPI(1).update_available())
