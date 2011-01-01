===========================
Documentation for Version 1
===========================

This is the prototype version for testing the backend/extension interaction.

Features
========

* Users are registered automatically without any password, only by a random id
* ratings are stored only in cumulative terms

API documentation
=================

``POST /1/register``
--------------------

Registers a new user and returns a ``userid`` for that user which can be stored
in the extension. This means that you will have different accounts on different
browsers. This will be changed in a future version.

Just ``POST`` to the URL to create a new user::

    POST ``/1/register``

This returns a new ``userid``::

    {
        'userid' : 'c6s8c76s87cs68cd76cs8c7s68cs76d76'
    }

``POST /1/domains/<domain>``
----------------------------

To rate a site you post the ``rating`` to the ``domain``::

    POST /1/domains/comlounge.net
    Content-Type: application/json

    {
        'rating' : 0,
        'userid' : 'c6s8c76s87cs68cd76cs8c7s68cs76d76'
    }


``domain`` is a string containing the domain name and ``rating`` is an integer
which is either 0, 6, 12, 16 or 18. ``userid`` is the user id of the user who
rates.

``GET /1/domains/<domain>``
---------------------------

To retrieve the current rating for a domain you just GET it. This will return
the following JSON document::

    {
        'rating' : 6
    }

If multiple ratings are present then the one with the most votes will be
returned. If no one wins, then null will be returned instead. 





