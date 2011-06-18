= rnaseq.pyramid =

This is a Pyramid server that serves the public pages of the RNASeq homepage.

For more information about Pyramid, check out the official website:

    http://pylonsproject.org/

= Starting the server =

For information on starting and stopping the server, have a look at the README.txt
in rnaseq.buildout:

svn://mroder@svn.crg.es/big/rnaseq/rnaseq.buildout/trunk

= About the server =

The only purpose of this module is to configure the pages of the project so that the
Pyramid application knows them and can serve them using the right models.

The configuration of the pages and boxes is imported from raisin.box and raisin.page:

    from raisin.page import PAGES
    from raisin.box import BOXES

The models are imported from rnaseq.restyler:

    from rnaseq.restyler.page import Page
    from rnaseq.restyler.box import Box

See the respective packages to learn about how to customize the pages and boxes.

All you need to know is that Pyramid is able to render all pages, and also renders all
boxes that appear in the pages individually, and in different formats. The Pyramid
server does not know about these formats, it just configures routes to them.
