# EN 26-11: 66 sentences, 07:20

[VOZ SIN TRANSCRIBIR] 05:33-05:40: leer en en_captions.png

## block 0 topic 0 presenter 00:00-00:05
[00:00] Hello, my name is Rainer Hanekamp and this is NG News with the latest updates from the Angular community every week.

## block 1 topic 1 presenter 00:05-00:29
[00:05] TypeScript version 6 is out.
[00:07] And as already mentioned in a few episodes before, that one is the last version which is written in TypeScript itself.
[00:15] The next one will be written in Go.
[00:18] For us as Angular developers, in Angular version 21, we have still TypeScript 5 .9 as a peer dependency, but in the git branches for version 22, they already have TypeScript 6.

## block 2 topic 1 screen 00:29-00:34

## block 3 topic 1 presenter 00:34-00:51
[00:33] Since TypeScript 6 is meant to be a bridge between the old and the new TypeScript versions, it comes with a lot of deprecations, but also pays tribute in terms of default settings, how the ecosystem works in 2026.

## block 4 topic 1 screen 00:51-01:38
[00:51] That means strict mode is on by default.
[00:54] The module option now defaults to ESNext.
[00:58] So in practice, you are in ECMAScript module land for new projects.
[01:02] And target floats to whatever is the current ECMAScript year track.
[01:06] Right now, that lands on ES2025 on the deprecation side.
[01:12] Target ES5 is on the way out.
[01:15] That is the world before classes, arrow functions, promise, let const, template strings, and all of that.
[01:23] For most of us, that is ancient history anyway.
[01:27] Base URL in the TS config is deprecated.
[01:31] Support for AMD, UMD, and System .js as module outputs is also deprecated.

## block 5 topic 1 presenter 01:38-02:12
[01:38] You can, of course, also opt out of all those deprecations.
[01:42] but be aware, in TypeScript 7, that would mean game over.
[01:46] It is also worth mentioning that there is an experimental migrator available from TypeScript 5 to 6.
[01:53] And TypeScript 6 is not just about deprecations, it also brought new features.
[01:59] And one of them is the Temporal API.
[02:03] That's a new date and time API, which is already standardized, and it is a replacement for the old date object.

## block 6 topic 1 screen 02:12-02:36
[02:12] As that, it provides way more functionality, for example, time zones, a calendar which can be used to reflect Chinese or other calendar systems, immutability, and a range of other utility functions.
[02:26] Some veterans of us might remember the switch to the datetime API in Java more than 10 years ago.
[02:33] In some way, it feels like that.

## block 7 topic 2 presenter 02:36-02:50
[02:36] that. ngRx is the most used state management library for Angular.
[02:40] And the official work for supporting resources but also signal forms has begun.
[02:47] Two new RFCs have been published.

## block 8 topic 2 screen 02:50-04:01
[02:50] The first RFC is related to supporting signal forms and it introduces a new signal type called delegated signal.
[02:58] To the outside, it is a writable signal, but it doesn't store value.
[03:03] Instead, it writes and reads to another signal.
[03:07] What's the use of it?
[03:08] Let's say we have a user object in a signal that has two nested properties, name and address.
[03:14] Name has first name and last name and address has street and city.
[03:17] If we have a form which requires a flattened version of the user object, we could usually create a linked signal.
[03:25] The problem is that that changes in the form might be synchronized back to the original signal.
[03:32] At the moment, the only way would be to use an effect, which would be asynchronous synchronization.
[03:40] Delegated signal, on the other hand, solves this problem by writing synchronously back to the original signal.
[03:47] The delegated signal can also be used for different use cases, but the story for the signal store is that if you use signal forms that each change of a form field immediately updates the state.

## block 9 topic 2 presenter 04:01-04:17
[04:00] In some way, you can see the delegated signal as a better linked signal where not a clone is created, but instead the change is directly written back to the original signal.
[04:13] And the other RFC is about supporting resources.

## block 10 topic 3 screen 04:17-04:39
[04:17] It allows to extend the resource which goes beyond the possibilities of the current snapshot function.
[04:24] For example, an extension would change the behavior of a resource in an error state, wherein access to the value does not throw.
[04:33] Custom extensions are possible as well, and there is even an option to define default extensions.

## block 11 topic 3 presenter 04:39-04:44
[04:39] The two RFCs were created by Marko Stanimirovic, and the same Marko was also guest at a previous episode in the Angular Plus show.

## block 12 topic 3 screen 04:44-04:56
[04:48] So if you're interested to hear more about state management and the signal store specifically, you should check out that episode.

## block 13 topic 4 presenter 04:56-05:12
[04:56] In other news, Martina Graus was guest at the Angular Plus show, and that means that the topic was about security.
[05:02] Together with the three hosts, Laura Newsome, Brooke Avery and Jan -Niklas Wortmann, they discussed the whole portfolio of security topics.

## block 14 topic 4 screen 05:12-05:48
[05:12] Be it trusted types, sanitization, attacks like cross -site scripting or cross -site request forgery, but also content policies and increased risk that comes with AI.
[05:23] At the end, Martina gave some tips where to start with security, and she also highlighted the OWASP juice shop, which is written in Angular and is a playground to try out different vulnerabilities.

## block 15 topic 5 presenter 05:48-06:11
[05:48] And we will get a third debounce option in Angular.
[05:50] The first one was the debounce function in signal forms, which means the debouncing happened between a form field and its model.
[06:00] The second one is the debounced function, which can be used for any signal.
[06:06] And the new one, the third one, is for the asynchronous validators in signal forms.

## block 16 topic 5 screen 06:11-06:31
[06:12] That allows you to have un -debounced synchronous validators, but apply debouncing on an asynchronous synchronous validator.
[06:20] That feature has been merged into the 22 version branch, but it didn't make it into the latest 21 .2 .7 version.
[06:28] So it seems we have to wait for Angular 22.

## block 17 topic 6 presenter 06:31-06:42
[06:31] Alfredo Perez published a three article series about spec driven development with AI.
[06:38] The probably most popular tool is GitHub's spec kit, which Alfredo describes.

## block 18 topic 6 screen 06:42-07:09
[06:44] But additionally, Additionally, he has created a VS Code extension called SpecKit Companion, not just to visualize, but also to edit and execute those specifications.
[06:57] Since GitHub SpecKit is not the only tool out there, Alfredo also shows alternatives and how SpecKit Companion can be configured to support those tools as well.

## block 19 topic 7 presenter 07:09-07:11
[07:08] Finally, the recording of the Angular Grads Meetup are available on YouTube.

## block 20 topic 7 screen 07:11-07:15
[07:13] YouTube, they are published in a regular interval.

## block 21 topic 7 presenter 07:15-07:20
[07:15] And that's it.
[07:16] I wish you a nice week and see you in the next episode.
[07:19] Goodbye.
