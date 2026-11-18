# Copyright (C) 2026 The MegaMek Team. All Rights Reserved.
"""Decide which MegaMek releases need a Docker image built.

Reads the MegaMek release list, picks the newest Core and the newest Experimental release,
and prints the build matrix the workflow runs. It builds nothing itself.

Modes:
    missing  build a release only when one of the registries has no image for it (daily run)
    rebuild  build the newest release of each channel again (weekly base image refresh)
    check    build the newest Core release without pushing (pull requests, dry runs)
"""

import argparse
import json
import os
import re
import subprocess
import sys

SOURCE_REPOSITORY = "MegaMek/megamek"
TAG_PATTERN = re.compile(r"^v(\d+(?:\.\d+){1,3})$")
CORE = "core"
EXPERIMENTAL = "experimental"
MODES = ("missing", "rebuild", "check")


def parse_version(tag):
    """Return the numeric parts of a release tag such as v0.51.00.1, or None when it is not one."""
    match = TAG_PATTERN.match(tag or "")
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def has_archive(release, version):
    """True once the release carries the MegaMek-<version>.tar.gz the Dockerfile downloads."""
    wanted = f"megamek-{version}.tar.gz"
    for asset in release.get("assets", []):
        if asset.get("name", "").lower() == wanted:
            return True
    return False


def usable_releases(releases):
    """Published releases with a version tag and a downloadable archive, newest version first."""
    usable = []
    for release in releases:
        tag = release.get("tag_name", "")
        numbers = parse_version(tag)
        if numbers is None or release.get("draft"):
            continue
        version = tag[1:]
        if not has_archive(release, version):
            continue
        usable.append({
            "release": tag,
            "version": version,
            "numbers": numbers,
            "channel": EXPERIMENTAL if release.get("prerelease") else CORE,
        })
    usable.sort(key=lambda entry: entry["numbers"], reverse=True)
    return usable


def newest_per_channel(usable):
    """Map each channel to its newest release. The input is already sorted newest first."""
    newest = {}
    for entry in usable:
        newest.setdefault(entry["channel"], entry)
    return newest


def tags_for(entry, is_newest, images):
    """Every image reference to push for one release.

    The version tag always goes out. The moving tags (core plus latest, or experimental) only
    go to the newest release of a channel, so building an old version never moves them back.
    """
    names = [entry["release"]]
    if is_newest:
        names.append(entry["channel"])
        if entry["channel"] == CORE:
            names.append("latest")
    return [f"{image}:{name}" for image in images for name in names]


def image_exists(reference):
    """Ask the registry whether an image reference exists."""
    result = subprocess.run(
        ["docker", "buildx", "imagetools", "inspect", reference],
        capture_output=True, text=True, check=False)
    return result.returncode == 0


def plan(releases, mode, images, version=None, exists=image_exists):
    """Return the list of builds for this run."""
    usable = usable_releases(releases)
    newest = newest_per_channel(usable)

    if version:
        wanted = version if version.startswith("v") else f"v{version}"
        chosen = [entry for entry in usable if entry["release"] == wanted]
        if not chosen:
            raise SystemExit(f"No published MegaMek release {wanted} with a tar.gz archive")
    elif mode == "check":
        chosen = [newest[CORE]] if CORE in newest else []
    else:
        chosen = [newest[channel] for channel in (CORE, EXPERIMENTAL) if channel in newest]

    builds = []
    for entry in chosen:
        is_newest = newest.get(entry["channel"]) is entry
        if mode == "missing" and not version:
            missing = [image for image in images if not exists(f"{image}:{entry['release']}")]
            if not missing:
                continue
        builds.append({
            "release": entry["release"],
            "version": entry["version"],
            "channel": entry["channel"],
            "tags": ",".join(tags_for(entry, is_newest, images)),
        })
    return builds


def fetch_releases():
    """Read the newest 100 MegaMek releases through the gh CLI."""
    result = subprocess.run(
        ["gh", "api", f"repos/{SOURCE_REPOSITORY}/releases?per_page=100"],
        capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main(arguments=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--images", default="",
                        help="Comma separated image names without a tag; empty entries are ignored")
    parser.add_argument("--version", default="", help="Build this release only, for example v0.51.00.1")
    parser.add_argument("--releases-file", default="",
                        help="Read the release list from a JSON file instead of GitHub")
    options = parser.parse_args(arguments)

    images = [image.strip() for image in options.images.split(",") if image.strip()]
    if options.releases_file:
        with open(options.releases_file, encoding="utf-8") as handle:
            releases = json.load(handle)
    else:
        releases = fetch_releases()

    builds = plan(releases, options.mode, images, options.version.strip() or None)

    if builds:
        for build in builds:
            print(f"Build {build['release']} ({build['channel']}): {build['tags'] or 'no push'}")
    else:
        print("Nothing to build: every current release already has an image.")

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as handle:
            handle.write(f"matrix={json.dumps({'include': builds})}\n")
            handle.write(f"has_builds={'true' if builds else 'false'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
