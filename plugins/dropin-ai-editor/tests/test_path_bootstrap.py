"""Every script's portable path bootstrap runs on its own and resolves kit paths."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = 'portable path bootstrap'
END = '# ── end bootstrap ──'


def bootstrap_blocks():
    for path in sorted(ROOT.rglob('*.py')):
        if '.venv' in path.parts or path.name == Path(__file__).name:
            continue
        lines = path.read_text().splitlines()
        starts = [i for i, line in enumerate(lines) if START in line]
        if not starts:
            continue
        end = next(i for i in range(starts[0], len(lines)) if lines[i].strip() == END)
        yield path, '\n'.join(lines[starts[0]:end + 1])


class PathBootstrapTests(unittest.TestCase):
    def test_bootstraps_were_found(self):
        self.assertGreater(len(list(bootstrap_blocks())), 40)

    def test_each_bootstrap_resolves_kit_paths(self):
        saved_path = list(sys.path)
        self.addCleanup(setattr, sys, 'path', saved_path)
        for path, block in bootstrap_blocks():
            with self.subTest(script=str(path.relative_to(ROOT))):
                scope = {'__file__': str(path), '__name__': 'bootstrap_check'}
                exec(compile(block, str(path), 'exec'), scope)
                for helper, arg in (('_acq', '_shared'), ('_acq', 'edit/scripts'), ('_acqv', 'SOPs')):
                    if helper in scope:
                        resolved = Path(scope[helper](arg))
                        self.assertTrue(str(resolved).startswith(str(ROOT)), resolved)


if __name__ == '__main__':
    unittest.main()
