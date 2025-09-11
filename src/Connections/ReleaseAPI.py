from requests import get
from os import mkdir, execv, remove
from shutil import rmtree
from subprocess import check_output
from datetime import datetime


class ReleaseAPI:
    """
    a class to check for software updates and handle updates
    a new version is detected when there is a new release on the GitHub releases page

    if a release needs to perform any installation steps aside from pulling the latest code
    an asset named update.sh should be included in the release with the required installation steps
    which will automatically by run by the installer

    all assets will be downloaded to ../patches/<release_tag> and can be accessed by the update.sh script
    which will run in the ../patches/<release_tag> directory
    also note that the patches directory will be deleted after the update is complete

    ** note that the directories above are relative to the src directory the program runs in **
    """

    REPO_URL = "https://api.github.com/repos/TB543/4RunnerDash/releases"

    def __init__(self, shutdown):
        """
        creates the release manager

        @param callback: the shutdown callback to call before updating
        """

        # sets fields
        self.callback = shutdown
        current_release = check_output(["git", "describe", "--tags", "--abbrev=0"]).decode("utf-8").strip()
        
        # pulls the latest release from GitHub
        try:
            releases = get(
                ReleaseAPI.REPO_URL,
                timeout=5
            ).json()

            # gets the list of releases newer than the current version
            current_release = next((release for release in releases if release["tag_name"] == current_release), None)
            current_release_date = datetime.strptime(current_release["published_at"], "%Y-%m-%dT%H:%M:%SZ")
            self.releases = [release for release in releases if datetime.strptime(release["published_at"], "%Y-%m-%dT%H:%M:%SZ") > current_release_date]
            self.releases.sort(key=lambda release: datetime.strptime(release["published_at"], "%Y-%m-%dT%H:%M:%SZ"))

        # returns the current release if there is no internet connection
        except Exception:
            self.releases = None

    def update_available(self):
        """
        checks if a new version is available

        @return: True if a new version is available, False otherwise
        """

        return self.releases
    
    def download_patch(self, patch):
        """
        downloads all the files for a given patch

        @param patch: the release patch to download
        """

        # installs the patch
        mkdir(f"../patches/{patch['tag_name']}")
        for asset in patch["assets"]:
            with open(f"../patches/{patch['tag_name']}/{asset['name']}", "wb") as f:
                f.write(get(
                    asset["browser_download_url"],
                    timeout=5
                ).content)

        # adds patch to update script
        with open(f"../patches/update.sh", "a") as f:
            f.write(f"\n# installs {patch['tag_name']}\n")
            f.write(f"cd {patch['tag_name']}\n")
            f.write("dos2unix ./update.sh\n")
            f.write("/bin/bash ./update.sh\n")
            f.write("cd ..\n")
        
    def update(self):
        """
        updates the software to the latest version
        """

        # creates the update directory
        mkdir(f"../patches")
        with open(f"../patches/update.sh", "w") as f:
            f.write("#!/bin/bash\n")

        # downloads required files
        try:
            with open("AppData/patch_notes.txt", "w") as f:
                for release in self.releases:
                    self.download_patch(release) if release["assets"] else None

                    # generates patch notes
                    f.write(f"============================== {release['name']} ==============================\n")
                    f.write(f"{release['body']}\n")
                    f.write("\n\n")
        
        # removes new version if error occurs
        except:
            rmtree(f"../patches")
            remove("AppData/patch_notes.txt")
            return

        # installs the new version
        self.callback()
        execv("/bin/bash", ["/bin/bash", f"../resources/update.sh", self.releases[-1]['tag_name']])
