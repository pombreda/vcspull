# -*- coding: utf-8 -*-
"""Tests for pullv.

pullv.tests.test_repo_git
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

import os
import logging
import tempfile
from .helpers import RepoTest
from ..repo import Repo
from ..util import run
logger = logging.getLogger(__name__)


class RepoSVN(RepoTest):

    def test_repo_svn(self):
        repo_dir = os.path.join(self.TMP_DIR, '.repo_dir')
        repo_name = 'my_svn_project'

        svn_repo = Repo({
            'url': 'svn+file://' + os.path.join(repo_dir, repo_name),
            'parent_path': self.TMP_DIR,
            'name': repo_name
        })

        svn_checkout_dest = os.path.join(self.TMP_DIR, svn_repo['name'])

        os.mkdir(repo_dir)

        run(['svnadmin', 'create', svn_repo['name']], cwd=repo_dir)

        svn_repo.obtain()

        tempFile = tempfile.NamedTemporaryFile(dir=svn_checkout_dest)

        run(['svn', 'add', tempFile.name], cwd=svn_checkout_dest)
        run(
            ['svn', 'commit', '-m', 'a test file for %s' % svn_repo['name']],
            cwd=svn_checkout_dest
        )
        self.assertEqual(svn_repo.get_revision(), 0)
        svn_repo.update_repo()

        self.assertEqual(
            os.path.join(svn_checkout_dest, tempFile.name),
            tempFile.name
        )
        self.assertEqual(svn_repo.get_revision(tempFile.name), 1)

        self.assertTrue(os.path.exists(svn_checkout_dest))