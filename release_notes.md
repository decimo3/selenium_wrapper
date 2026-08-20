# Fixed static version on package manifest

Replaced static package version, now it's dynamic on a pythonic way.

This fixes an issue with direct source-code installations, where pip uses the package manifest version, causing it to conflict with the actual version.
