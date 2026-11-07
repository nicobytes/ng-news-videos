# EN 26-17: 37 sentences, 04:57


## block 0 topic 0 presenter 00:00-00:07
[00:00] Hello, my name is Michael Small, and this is NG News with the latest updates from the Angular community.

## block 1 topic 0 screen 00:07-00:25
[00:07] PrimeNG, a popular UI component library, has announced that future major versions won't be available as open source anymore, except through a free community license for individuals, students, nonprofits, non -commercial open source projects, and small organizations.

## block 2 topic 0 presenter 00:25-00:30
[00:25] That doesn't just apply to the Angular version, but to the React and Vue versions as well.

## block 3 topic 0 screen 00:30-01:08
[00:30] The reason is that the library has grown over time, which means if you do this as an open source, you have to spend much more time on it, and at some point, the income that they got from selling things around the library itself
[00:42] didn't cover the costs anymore.
[00:44] The new licensing brand is Prime UI.
[00:47] The launch price is $599 USD per developer.
[00:52] That is perpetual, so for life for the covered versions, and includes one year of updates.
[00:58] It includes Prime UI Pro, which contains components for charts, text editor, scheduler, task board, and more.

## block 4 topic 0 presenter 01:08-01:12
[01:07] The Pro components are not part of the community license.

## block 5 topic 0 screen 01:12-01:37
[01:12] That being said, OpenNG, which maintains unmaintained libraries, announced that PrimeNG went closed source.
[01:20] source. The GitHub repository was archived on June 28, 2026, and OpenNG created a copy of the project with regenerated open issues and PRs.
[01:31] Their goal is to release a beta version supporting Angular 22 for the fork.

## block 6 topic 0 presenter 01:37-01:48
[01:37] At the time of this writing, the current name is outstanding as OpenNG does not want to be too close to PrimeNG because Primetech plans hands to put trademarks on it.

## block 7 topic 1 screen 01:48-01:59
[01:49] Devon Chastanoff from the Angular team has published an article on how to use A2UI with Angular, which enables dynamic UI that is controlled by an AI model.

## block 8 topic 1 presenter 01:59-02:02
[01:59] The user expresses an intent through the front end.

## block 9 topic 1 screen 02:02-02:26
[02:02] Front end sends that intent in relevant context to a model.
[02:05] This communication can also include a component catalog that the front end knows how to render.
[02:11] The model can then decide whether UI components are needed, which components are appropriate, and return structured UI instructions to the application.
[02:21] A2UI is a protocol used for these agent -generated UI use cases.

## block 10 topic 2 presenter 02:26-02:32
[02:26] In other news, work on integrating resource behavior with the router seems to have begun.

## block 11 topic 2 screen 02:32-03:06
[02:32] PR meant for internal usage at the moment popped up, which uses a snapshot -like router resource behavior to integrate great navigation specific information.
[02:42] That snapshot would freeze a resource's state, for example, the value, while a navigation happens.
[02:49] Once the navigation succeeds, the underlying value is exposed.
[02:54] And if a navigation is canceled, the frozen value would still be there during rollback recovery.
[03:00] Now imagine the following use case without this router resource behavior.

## block 12 topic 2 presenter 03:06-03:40
[03:07] Regular old resource has a router parameter as its own parameter.
[03:11] That could be a product ID which loads the product by its given ID.
[03:15] If the user stays on the same component but navigates to a different product ID, the resource would immediately change its state and the UI would change while the navigation happens.
[03:27] That would cause flickering effects, especially if the navigation gets cancelled via guard and the product ID changes back to its initial value.
[03:35] With the introduced router resource source behavior that is not going to happen.

## block 13 topic 2 screen 03:40-03:54
[03:40] Again, PR's description explicitly states that this is not currently exposed for public use, but it is very likely the start of getting resources and the router working together.

## block 14 topic 3 presenter 03:54-04:04
[03:54] In other news, going with micro front -ends is an architectural choice, which we find often in enterprises.

## block 15 topic 3 screen 04:04-04:27
[04:01] Although they are not an Angular framework feature, feature, there are two common community solutions in the form of Native Federation and Module Federation.
[04:11] The main distinction in Angular is that Native Federation works with ESBuild, so the modern Angular builder, and Module Federation traditionally works with the old Webpack builder or alternative builders such as RSPack.

## block 16 topic 3 presenter 04:27-04:36

## block 17 topic 3 screen 04:36-04:51
[04:26] native federation is maintained by angular architects and module federation support in nx has been common for angular workspaces in the release blog for nx 23 nx now recommends angular architects native federation package for angular and deprecates the older nx specific module federation generators

## block 18 topic 3 presenter 04:51-04:58
[04:49] and executors and that's it i wish you a nice week and see you in the next step so goodbye
