# alfred-web-links

This is a script for defining Alfred shortcuts in code, rather than through the GUI interface.
More specifically, it lets me create web bookmarks by writing a YAML file.

It creates a .alfredworkflow bundle.

## Why do this?

1.  I wanted to see if I could build Alfred workflows programatically.
    (Spoiler: I can!
    A .alfredworkflow file is just a ZIP bundle with a particular structure.)

2.  I generally prefer things which are managed "in code", not through GUIs.

3.  I use Alfred on my home and my work computer, but I don't sync Dropbox between them.
    Storing the workflow in GitHub and building it on the fly lets me share config without syncing Dropbox.

## Usage

You need Git, make and Docker installed.

To build the workflow:

```console
$ git clone git@github.com:alexwlchan/alfred-web-links.git
$ make data/web-links.alfredworkflow
```

You then open web-links.alfredworkflow and install it in Alfred.

To add new links, you need to edit [data/alfred-web-links.yml](data/alfred-web-links.yml), re-run the make task, and install the updated package.
