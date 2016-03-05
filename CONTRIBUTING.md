This document describes how the 18F eRegs team has agreed to work together
with regard to Git, GitHub and facilitating changes to the repositories they
administer.

## Workflow

The most common workflow is:

1. A change is initiated and discussed via a GitHub issue or Trello card.
1. Team members discuss prioritization in daily standup and claim tasks.
1. A Pull Request (PR) is created on Github. The related GitHub issue or Trello
   card is referenced in the PR description.
1. The PR is reviewed by someone other than the committer.
1. Once PR feedback has been addressed and/or incorporated, the reviewer merges
   the pull request.
1. When the Travis CI build passes on `master`, updates are automatically
   deployed to the staging environment.

## Coding standards

* Use [PEP8](https://www.python.org/dev/peps/pep-0008/) as the coding standard
  for Python.
* Use Sphinx-style docstrings for function and method documentation, including
  signatures, unless they're very short. See
  http://www.sphinx-doc.org/en/stable/domains.html#signatures for details.
* Add inline comments for things that aren't intuitive.
* If you can re-write something to be more intuitive, that is preferable to
  adding comments.
* Follow the boy scout rule: "Always leave the code cleaner than you
  found it."

## Code review guidelines

* The author and reviewer have equal responsibility for code.
* Don't merge things until you are confident you could maintain it as-written.
* Reviewers expect code to be submitted with test coverage.
* Travis CI runs the test suite and a PEP8 linter on GitHub PRs. PRs should only
  be merged when Travis is green.

## Forking vs Branching

This team prefers forking.

The rationale for preferring forking is that all contributors work the same way,
regardless of whether or not they may commit directly to the canonical
repository.

If a feature requires collaboration from several team members, a git branch may
be easier than a fork and is an acceptable alternative in that situation.

## Squashing / rebasing commits

Individual contributors may choose to rebase and [squash
commits](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History#Squashing-Commits)
to clean up git history on a fork that is being PR'd. It is not expected or
required for contributors to change their git history.

## When should a PR be created?

This team opens PRs for all commits, even typos.

Exceptions may be granted in the case of an imminent deploy. The team should be
consulting before pushing code directly to master.

When pairing, a pair may self-merge work but should open a pull request before
merging to create a record of the work being merged.

## When reviewing a PR, should the change be tested locally?

This team does not have a standard QA process.

## Team processes

* Don't merge your own pull request. Find a friend to review your code and merge your pull request.
* Pull requests should contain some tests. Ideally they would contain decent test coverage.
* If you make changes to the API, please help update the API documentation. 

When creating a new pull request:

* If the pull request is still a work-in-progress and should not be merged, say
  so in the description.
* Anyone is welcome to informally review a PR and comment on it at any time, no
  matter who is assigned.

## Public domain

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
