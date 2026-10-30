# Installation and maintenance

Keep a clone as the maintained source. Check out the desired release tag, run
checks, preview installation, then apply. The installer downloads nothing and
does not edit global Codex configuration. The default personal skill location is
~/.agents/skills/math-paper-editor; --dest selects an explicit alternative.
Avoid duplicate discoverable installations.

## Adopting an older unmanaged installation

Create a **private** JSON map of the existing installation's relative file paths
to SHA-256 values after reviewing those files. Supply --legacy-baseline FILE
to preview and then --apply to replace that exact version. Changed or extra files
invalidate the baseline. Do not commit this private baseline.

The entire legacy installation is retained in a timestamped backup outside skill
discovery, including old documentation/examples. The public helper uses record
schema 2. Finish pre-public schema-1 runs using the original helper retained in
that backup. Manuscript audit directories are never searched or migrated.

## Managed upgrades

~~~sh
git fetch --tags origin
git checkout v0.1.0
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 tools/install.py
python3 tools/install.py --apply
~~~

Choose a later published tag when upgrading. Modified/deleted managed files or
unmanaged collisions stop the upgrade. Compare and merge customization first.
Other unmanaged extras are retained. Backups default to
~/.agents/skill-backups/math-paper-editor; --backup-root overrides it.
Generated Python caches and platform metadata are excluded from managed files
and the new installed copy.

Installation stages files, rechecks source and destination hashes, moves the old
installation to backup, and renames the staged directory into place. Failure
before installing the new directory restores the previous directory when safe.
This does not lock other editors. Use a local filesystem with the backup on the
same filesystem as the installed directory.

For rollback, review the backup and current installation first. Restore only
after accounting for subsequent local changes. Backups are not deleted
automatically.
