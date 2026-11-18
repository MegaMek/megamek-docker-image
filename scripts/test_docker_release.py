# Copyright (C) 2026 The MegaMek Team. All Rights Reserved.
"""Tests for docker_release.py. No network and no Docker: registry lookups are faked."""

import unittest

import docker_release

GHCR = "ghcr.io/megamek/megamek"
MIRROR = "registry.example/megamek"


def release(tag, prerelease=False, draft=False, archive=True):
    assets = [{"name": f"MegaMek-{tag[1:]}.tar.gz"}] if archive else []
    return {"tag_name": tag, "prerelease": prerelease, "draft": draft, "assets": assets}


RELEASES = [
    release("v0.51.01.9", prerelease=True),
    release("v0.51.01.10", prerelease=True),
    release("v0.51.01", draft=True),
    release("v0.51.00.1"),
    release("v0.51.0"),
    release("nightly"),
]


def registry(*present):
    return lambda reference: reference in present


class ParseVersionTest(unittest.TestCase):
    def test_numbers_compare_as_numbers_not_text(self):
        self.assertGreater(docker_release.parse_version("v0.51.01.10"),
                           docker_release.parse_version("v0.51.01.9"))

    def test_rejects_tags_that_are_not_versions(self):
        self.assertIsNone(docker_release.parse_version("nightly"))
        self.assertIsNone(docker_release.parse_version("0.51.0"))


class PlanTest(unittest.TestCase):
    def test_missing_mode_builds_newest_of_each_channel(self):
        builds = docker_release.plan(RELEASES, "missing", [GHCR, MIRROR], exists=registry())
        self.assertEqual(["v0.51.00.1", "v0.51.01.10"], [build["release"] for build in builds])
        self.assertEqual(["core", "experimental"], [build["channel"] for build in builds])

    def test_core_gets_latest_and_experimental_does_not(self):
        builds = docker_release.plan(RELEASES, "missing", [GHCR], exists=registry())
        self.assertEqual(f"{GHCR}:v0.51.00.1,{GHCR}:core,{GHCR}:latest", builds[0]["tags"])
        self.assertEqual(f"{GHCR}:v0.51.01.10,{GHCR}:experimental", builds[1]["tags"])

    def test_missing_mode_skips_a_release_present_everywhere(self):
        present = registry(f"{GHCR}:v0.51.00.1", f"{MIRROR}:v0.51.00.1", f"{GHCR}:v0.51.01.10")
        builds = docker_release.plan(RELEASES, "missing", [GHCR, MIRROR], exists=present)
        self.assertEqual(["v0.51.01.10"], [build["release"] for build in builds])

    def test_rebuild_mode_ignores_the_registry(self):
        builds = docker_release.plan(RELEASES, "rebuild", [GHCR], exists=lambda reference: True)
        self.assertEqual(2, len(builds))

    def test_check_mode_builds_core_only_with_nothing_to_push(self):
        builds = docker_release.plan(RELEASES, "check", [], exists=registry())
        self.assertEqual(["v0.51.00.1"], [build["release"] for build in builds])
        self.assertEqual("", builds[0]["tags"])

    def test_drafts_and_releases_without_an_archive_are_ignored(self):
        releases = [release("v0.52.0", archive=False), release("v0.51.5", draft=True), release("v0.51.0")]
        builds = docker_release.plan(releases, "rebuild", [GHCR])
        self.assertEqual(["v0.51.0"], [build["release"] for build in builds])

    def test_named_old_version_does_not_move_the_channel_tags(self):
        builds = docker_release.plan(RELEASES, "missing", [GHCR], version="0.51.0",
                                     exists=lambda reference: True)
        self.assertEqual(f"{GHCR}:v0.51.0", builds[0]["tags"])

    def test_named_newest_version_moves_the_channel_tags(self):
        builds = docker_release.plan(RELEASES, "missing", [GHCR], version="v0.51.00.1")
        self.assertIn(f"{GHCR}:latest", builds[0]["tags"])

    def test_unknown_version_fails(self):
        with self.assertRaises(SystemExit):
            docker_release.plan(RELEASES, "missing", [GHCR], version="v9.9.9")


if __name__ == "__main__":
    unittest.main()
