# keep-todoist-sync

In August 2022, Google/IFTTT rolled out "changes" that completely nerf'd the integration:
https://ifttt.com/explore/google-assistant-changes

Amongst many things, you can no longer have trigger phrases with variables in them.
That meant you can no longer create applets like:
When I say "Okay Google, take a note 'clean out the BBQ'", create a task in my [Todoist](https://todoist.com) inbox called "clean out the BBQ".

This was the applet/feature I most used on Google Assistant by far.

It looks like now, saying "take a note" creates a note in one of 3 applications (including Google Keep).

Since Google Keep has no official API, I don't think any commercial automation offering integrates with it.

This, I created this simple project which uses [gkeepapi](https://gkeepapi.readthedocs.io/en/latest/#) and the Todoist python [SDK](https://developer.todoist.com/rest/v2/?python#python-sdk)
to essentially replicate the same behavior, albeit a little slower due to the polling nature.
