# EN 26-21: 46 sentences, 07:41

[VOZ SIN TRANSCRIBIR] 01:40-01:43: leer en en_captions.png
[VOZ SIN TRANSCRIBIR] 02:55-02:57: leer en en_captions.png
[VOZ SIN TRANSCRIBIR] 05:07-05:09: leer en en_captions.png

## block 0 topic 0 presenter 00:00-00:06
[00:00] Hello, my name is Rainer Hanekamp and this is NG News with the latest updates from the Angular community.

## block 1 topic 2 presenter 00:06-00:33
[00:05] Angular 20 .2 .2 is out and since we are only getting one major per year, that means that features in miners are also quite noteworthy.
[00:18] In our case, that is the router resource, the new error boundaries, both features in developer preview, but also the possibility that private properties can be accessed from the template let's start first with the router resource so we see here we have a we

## block 2 topic 3 presenter 00:33-00:49
[00:39] have a holidays page and it is using a service which generates a resource that this component is then using so if we go back to our application we see once the holidays are shown the different holiday cards are here also shown the issue

## block 3 topic 7 presenter 00:49-00:56

## block 4 topic 9 presenter 00:56-00:58

## block 5 topic 12 presenter 00:58-01:16
[00:59] is that the resource first of all starts when we entering the holidays page the component and this component also needs to deal with the loading state where maybe the value is not there and this is why we could now use the router resource

## block 6 topic 13 presenter 01:16-01:34
[01:16] so i could not define the same resource in the router which means the router would block until the data got loaded and then our page or component would get the final value

## block 7 topic 14 presenter 01:34-01:43
[01:32] so we would then have here the resources and then i would access here my holiday service
[01:39] with inject and

## block 8 topic 23 presenter 01:43-02:03
[01:43] i would then return here the resource what i need to do because my component will receive the value the loaded value of the resource of course via a certain name i have to provide here an object literal where i define under which name

## block 9 topic 24 presenter 02:03-02:09

## block 10 topic 25 presenter 02:09-02:35
[02:01] i want to register that value so i wouldn't say here these are the holidays context is also available as we see here we're getting here query parameters the normal parameters they are available as a signal in the case that they act as parameters
[02:19] for the resource itself so if we have an id in a url and that id is changing then we want to provide that id as a signal to the resource so that it gets automatically updated for

## block 11 topic 26 presenter 02:35-02:46
[02:34] us in the component what i need to do now is that i say okay these holidays there they are just a simple input property so i wouldn't say i have here i'm required, where

## block 12 topic 28 presenter 02:46-02:52

## block 13 topic 30 presenter 02:52-02:56
[02:51] I'm requesting not the resource, but the holiday array.

## block 14 topic 31 presenter 02:56-03:06
[02:57] And since we're doing a property binding, I also need to make it public.
[03:03] Last step, I need to go into my config.

## block 15 topic 34 presenter 03:07-03:13

## block 16 topic 35 presenter 03:13-03:15

## block 17 topic 37 presenter 03:15-03:21
[03:07] And I have to explicitly enable the router resources via the provider, why they provide router with router resources that's it if I now go back click on home click on holidays it is loaded and as I said before the loading now starts very

## block 18 topic 41 presenter 03:21-03:24

## block 19 topic 43 presenter 03:24-03:39
[03:28] early already in the router navigation itself and the component gets the final value it doesn't even know as you have seen that it actually is getting the value from a resource let's come to the second feature which are the error boundaries so we

## block 20 topic 47 presenter 03:39-03:42

## block 21 topic 48 presenter 03:42-04:10
[03:46] see here we have here first of all an app title component and the app holiday card so two child components
[03:54] if for some reason one of these child components throws an error then also our parent components have a problem so let me quickly go to the title component we have here my constructor constructor.
[04:08] And for some reason, I'm saying I'm just throwing here some kind of an error.

## block 22 topic 54 presenter 04:10-04:13

## block 23 topic 57 presenter 04:13-04:15

## block 24 topic 59 presenter 04:15-04:27
[04:13] If I now go back, and I click here on holidays, we see nothing is loaded, I mean loaded, nothing is shown anymore.
[04:22] And this is where these error boundaries become quite handy.

## block 25 topic 62 presenter 04:27-04:35
[04:26] Because now I can isolate the error.
[04:30] And the way how I do it is via the template.

## block 26 topic 63 presenter 04:35-04:40
[04:33] So I could say say this might be a risky sub component, then I just say I have here a boundary.

## block 27 topic 64 presenter 04:40-04:46
[04:41] In case the app title fails, the rest should be shown.

## block 28 topic 67 presenter 04:46-04:51
[04:46] So if I now go back, and again, click on holidays,

## block 29 topic 70 presenter 04:51-04:54
[04:51] then we see the holidays are shown.

## block 30 topic 73 presenter 04:54-05:03
[04:53] And I can also catch the error.
[04:56] Why are you using error?
[04:58] Of course, there are more options where I can also come up with conditional catches.

## block 31 topic 74 presenter 05:03-05:18
[05:02] matches. But we keep it here very simple.
[05:05] And then I could say here kind of a fallback
[05:09] component or template, where I would just say these are then the holidays, if something throws and I'll go back, we see holidays are shown as well.

## block 32 topic 81 presenter 05:18-05:22

## block 33 topic 84 presenter 05:22-06:43
[05:22] And the third main feature or change is the possibility that we can also access private properties in our templates.
[05:30] templates. So before 22 .2, this code would not have been possible.
[05:37] That I say I have your holidays, and that I then access that title signal from the template.
[05:45] That would have only worked if title would be public, or if it would have been protected.
[05:52] Which is why in a lot of code nowadays, we will probably see the protected which means only the template can access the variable with 22 .2 this is going to change as you see it just works and the reason is that it was
[06:10] important for the angular team that we understand from a conceptual point of view that the template the html and the typescript class they actually form form one unit, it's not two separate parts, it is one unit.
[06:26] So we'll see that with modern Angular code, more private keywords are used.
[06:33] And what we'll also see that the ECMAScript private will go away.

## block 34 topic 85 presenter 06:43-07:01
[06:39] Because if I use the ECMAScript private with the hash notation, that means it's also private during runtime, then this is not working.
[06:50] So I'm getting here also an error which of course means i have to let go of the ECMAScript one and have to use the normal private keyword in the future and that's it for the three main features of Angular 22 .2 for obvious

## block 35 topic 87 presenter 07:01-07:06

## block 36 topic 90 presenter 07:06-07:14

## block 37 topic 93 presenter 07:14-07:21
[07:06] reasons the router resources and the error boundaries they have much more options than i have shown this is just the basic functionality of them and yeah we also got other features in that release as well but here if you want to know more

## block 38 topic 96 presenter 07:21-07:29

## block 39 topic 99 presenter 07:29-07:36
[07:25] please consult the official documentation the changelog and of course from the community we also have a lot of content in the form of videos videos articles etc that's it i wish you a nice weekend see you in the next episode goodbye

## block 40 topic 102 presenter 07:36-07:41
