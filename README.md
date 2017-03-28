[![Dependencies](https://david-dm.org/jadedgamer/alifewellplayed.com.svg)](https://david-dm.org/jadedgamer/alifewellplayed.com)
[![Dependency Status](https://gemnasium.com/badges/github.com/jadedgamer/alifewellplayed.com.svg)](https://gemnasium.com/github.com/jadedgamer/alifewellplayed.com)


# A Life Well Played
=======

A Life Well Played is a CMS/Blog project written in Python/Django.

Interested on cloning the site for your own blog, similar or otherwise? Go for it. If you do make something with ALWP or Replica, send me a note, I'd love to see it.

---

## Replica (Version 2.0.0)
=======

Replica is a Django content management system I originally wrote for clients who wanted a simple and straight forward solution for posting updates. Since then, I've been slowly expanding and rebuilding it. Specifically, it's a a series of apps bundled tightly together.

### Features
* Automatic thumbnail generation for uploaded images
* Channels (Post Types). Assign posts different level of importance and style
* Topics. Assign any number topics/categories to posts. All topics have their own settings, including thumbnail images.
* Drafts. All revisions for entries are saved and can be compared to the most recent content.
* Markdown Support. Replica uses a simple markdown editor which even allows you to preview content with a click of a button.
* Quick post. Quickly jot down an idea from the front page of the dashboard, and expand on it later on.
* Responsive. The Dashboard is mobile friendly, in both reviewing and publishing new content.
* API. Replica features a RESTful API.

### Status
Replica has been rebuilt from the ground up, and is currently a work in progress. It's recommended you use at your own risk. You should probably have a good understanding of Django if you want to incorporate this into your project. File and database structure is also still a work in progress, and major Migrations may still happen.

### Contribute
My immediate priority is the completion of the dashboard, better unit tests and docs, but feel free to send pull requests on bug fixes you might find.

### Support
This software is provided 'as-is'. I can not help you get this working with your project, or offer any kind of support at this moment. If you believe you encountered a bug, open an [issue on Github](https://github.com/underlost/alifewellplayed.com/issues).

### License
Replica is released under the [MIT License](LICENSE).
