# Contributing to palau.lims

Third-party contributions are essential for keeping `palau.lims` continuously
improving. We want to keep it as easy as possible to contribute changes that
get things working in your environment. There are a few guidelines that we need
contributors to follow so that we can have a chance of keeping on top of
things.

The following is a set of guidelines for contributing to `palau.lims`. These
are just guidelines, not rules. Use your best judgment, and feel free to
propose changes to this document with a 
[pull request](#how-to-submit-a-pull-request).

## Code of Conduct

This project adheres to the Contributor
Covenant [code of conduct][code of conduct]. By participating, you are expected
to uphold this code. Please report unacceptable behavior.

## Reporting an issue

Have you found a bug in the code which is not in the
[list of known bugs][issues]? Then, by all means please
[submit a new issue][new issue], and do not hesitate to comment on existing
[open issues][issues].

When filling a new issue, please remember to:

* **Use a clear and descriptive title** for the issue to identify the problem.

* **Describe the exact steps which reproduce the problem** in as many details
  as possible. For example, start by describing your computing platform (
  Operating System and version, how did you installed senaite.core and its
  dependencies, what file or front-end are you using as a signal source, etc.).
  You can also include the configuration file(s) you are using, or a dump of
  the terminal output you are getting. The more information you provide, the
  more chances to get useful answers.

* **Please be patient**. Depending on the service contracting modality hired,
  it can take some time to the Developer Team to reach your issue.

* If you opened an issue that has been resolved, it is a good practice to
  **close it**.

Remember to tag the issue with the label "bug" as well as with one of the
[available labels][labels] for the categorization by priority: `P0: critical`,
`P1: urgent`, `P2: very important`, `P3: important`, `P4: nice to have`.

## Requesting an improvement

Do you have a suggestion for improvement? Follow exactly the same procedure
explained on [Reporting an issue](#reporting-an-issue), but describe the
functionality you want to achieve instead of the problem you want to address.
Also, tag the ticket with the label "improvement" or "addition".

## Contributing to the source code

### Preliminaries

1. If you still have not done
   so, [create your personal account on GitHub][join].

2. [Fork this repository][fork]. This will copy the whole repository into your
   personal account at GitHub.

3. Then, go to your favourite working folder in your computer and clone your
   forked repository by typing (replacing ```YOUR_USERNAME``` by the actual
   username of your GitHub account):
   
   ```shell
   $ git clone https://github.com/YOUR_USERNAME/palau.lims
   ```

4. Your forked repository https://github.com/YOUR_USERNAME/palau.lims
   will receive the default name of `origin`. You can also add the original
   `palau.lims` repository, which is usually called `upstream`:

   ```shell
   $ cd palau.lims
   $ git remote add upstream https://github.com/beyondessential/palau.lims.git
   ```

To verify the new upstream repository you have specified for your fork, type
`git remote -v`. You should see the URL for your fork as `origin`, and the URL
for the original repository as `upstream`:

```shell
$ git remote -v
origin    https://github.com/beyondessential/palau.lims.git (fetch)
origin    https://github.com/beyondessential/palau.lims.git (push)
upstream  https://github.com/beyondessential/palau.lims.git (fetch)
upstream  https://github.com/beyondessential/palau.lims.git (push)
```

### Start working on your contribution

Checkout the `master` branch of the git repository in order to get synchronized
with the latest code:

```shell
$ git checkout master
$ git pull upstream master
```

Then create a local branch where you will add your changes:

```shell
$ git checkout -b my_feature
```

Now you can do changes, add files, do commits (please take a look at
[how to write good commit messages][how to write good commit messages]
and push them to your repository:

```shell
$ git push origin my_feature
```

If there have been new pushes to the `master` branch of the `upstream`
repository since the last time you pulled from it, you might want to put your
commits on top of them (this is mandatory for pull requests):

```shell
$ git remote update
$ git pull --rebase upstream master
```

Alternatively, you can merge upstream's `master` into your branch:

```shell
$ git remote update
$ git merge --no-ff upstream master
```

Although a merge is safer than rebase, the latter eliminates the unnecessary
merge commits required by `git merge` and makes the project history easier to
navigate. We strongly encourage the developer to know in detail the
differences, pros and cons between doing a `gir rebase` or `git merge`. Good
documentation on this regard can be found in
the [Atlassian's Merging vs. Rebasing tutorial][merging vs rebasing].

Note this `git rebase` or `git merge` is required for keeping your branch
aligned with the latest code from the repos. The incorporation of your work
into`master` through a Pull Request will always be done using `git merge`.

After the local branch `my_feature` has been pushed and you don't plan to add
more changes, you can change to the master branch again:

```shell
$ git checkout master
```

### How to submit a pull request

When the contribution is ready, you can [submit a pull request][compare]. Head
to your GitHub repository, switch to your `my_feature` branch, and click the
_**Pull Request**_ button, which will do all the work for you. Ensure the
comparison is done with the `master` branch unless you forked from another one.

Once a pull request is sent, the Developer Team will review the set of changes,
discuss potential modifications, and even push follow-up commits if necessary.

Some things that will increase the chance that your pull request is accepted:

* Write tests.
* Follow [Plone's Python styleguide][plone's python styleguide].
* Write a descriptive and detailed summary. Please consider that reviewing pull
  requests is hard, so include as much information as possible to make your
  pull request's intent clear.
* Do not address multiple bugfixes or features in the same Pull Request.
* Include whitespace and formatting changes in discrete commits.
* Add a changelog entry in the [changelog][changelog]

For more details about Git usage, please check out Chapters 1 and 2 from
[Pro Git book][git book].


[code of conduct]: code_of_conduct.md
[issues]: https://github.com/beyondessential/palau.lims/issues
[new issue]: https://github.com/beyondessential/palau.lims/issues/new
[labels]: https://github.com/beyondessential/palau.lims/labels
[join]: https://github.com/join
[fork]: https://github.com/beyondessential/palau.lims/fork
[how to write good commit messages]: https://chris.beams.io/posts/git-commit/
[merging vs rebasing]: https://www.atlassian.com/git/tutorials/merging-vs-rebasing
[compare]: https://github.com/beyondessential/palau.lims/compare/
[plone's python styleguide]: https://docs.plone.org/develop/styleguide/python.html
[changelog]: changelog.rst
[git book]: https://git-scm.com/book/en
