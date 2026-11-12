# EN 26-22: 59 sentences, 07:30


## block 0 topic 0 presenter 00:00-00:06
[00:00] Hello, my name is Rainer Haneckamp and this is NG News with the latest updates from the Angular community.

## block 1 topic 4 presenter 00:06-00:11
[00:05] Angular code is not directly compiled by TypeScript.

## block 2 topic 9 presenter 00:11-00:33
[00:09] Instead, it uses an Angular compiler which sits on top of TypeScript.
[00:15] TypeScript 7 is the latest version and it has been rewritten in Go.
[00:20] And it promises 10 times more performance in terms of compilation.
[00:26] And of course, such a big change to TypeScript also has a huge impact on Angular.

## block 3 topic 10 presenter 00:33-00:44
[00:34] Angular uses, the Angular compiler uses a programmatic API to parse and also to modify our TypeScript code.

## block 4 topic 12 presenter 00:44-01:02
[00:45] In some way, you can see the programmatic API as just Angular imports TypeScript like a library.
[00:52] Now, the thing is that this programmatic API is not available for TypeScript 7.

## block 5 topic 13 presenter 01:02-01:12
[01:00] It's not really a problem because TypeScript 7 .0 is compatible to TypeScript 6, which means Angular can use the TypeScript 6 programmatic API.

## block 6 topic 14 presenter 01:12-01:14

## block 7 topic 15 presenter 01:14-01:17

## block 8 topic 16 presenter 01:17-01:23

## block 9 topic 18 presenter 01:23-01:37
[01:17] so if angular wants to support typescript 7 .1 it has to use the programmatic api but here's the problem english written in typescript and all of a sudden it needs to use a library from an application which has been written in go now

## block 10 topic 19 presenter 01:37-02:06
[01:35] typescript will fix this via an interop api but that one will not support the transform api which actually angular requires
[01:47] Now, the plan is that Angular is going to use Oxy, which is written in Rust and already used by very popular tools like Vite.
[01:58] Roughly summarized, Angular uses Oxy to parse and prepare its compilation steps.

## block 11 topic 20 presenter 02:06-02:13
[02:07] What we need to know is that Angular has two different pipelines.

## block 12 topic 28 presenter 02:13-02:28
[02:11] The first one, Angular takes, for example, decorators and other things in TypeScript and maps the code into a TypeScript code, which it then serves to the TypeScript compiler.

## block 13 topic 29 presenter 02:28-02:50
[02:27] The other one is for type checking only.
[02:29] So this is where also the template is compiled in a very specific format where the TypeScript compiler can run checks on it.
[02:40] in the end both will then be executed by the typescript compiler itself which means we will gain this new improvements in terms of speed at the time of this writing the pr has already been merged into main so we might already get a

## block 14 topic 31 screen 02:50-03:03
[02:57] version of it in the upcoming version 22 .3 of of Angular.

## block 15 topic 34 presenter 03:03-03:34
[03:03] Developing native applications for Angular hasn't been a joy for us.
[03:08] Of course we have Ionic, but that one renders to a web view, which requires a middleware.
[03:16] We also have NativeScript, which is using native UIs, but we really never had something like React React Native with a production -proven renderer and a huge ecosystem like Expo, which supports the whole development lifecycle.

## block 16 topic 34 screen 03:34-03:50
[03:34] On September the 29th, this changed.
[03:38] Angular Native was released by Ashley Hunter and has gained some traction in terms of contributors.
[03:45] It is an independent community project and is currently in alpha.

## block 17 topic 35 presenter 03:50-04:12
[03:50] The great thing is that React Native's renderer, which is called Fabric, does not depend on React.
[03:58] So what happens usually is that React tells Fabric what kind of parts in the component tree have to be changed.
[04:08] And now Ashley's idea was to use an Angular renderer instead of React.

## block 18 topic 39 presenter 04:12-04:54
[04:14] So the Angular renderer usually talks to the DOM, but you can write your own renderer so that it now talks to Fabric.
[04:22] This idea of using a different renderer has already been proven in the past.
[04:28] For example, Chow Tran uses the same approach in his library Angular 3.
[04:33] For us, that means that we can build on top of a bulletproof renderer implementation, which is well maintained.
[04:42] And with Angular Native, we have now a community project, which provides the integration by using official extensions to Angular's renderer.

## block 19 topic 40 screen 04:54-06:02
[04:53] Since it is native and not DOM, again, Ionic uses a web view.
[04:59] We also cannot just use existing components or UI libraries that depend on the browser.
[05:05] For native UI, we have to use the native Native ones, familiar tags like div and p do work, but they are mapped to native views and text.
[05:17] There is an exception though.
[05:19] DOM component lets us embed existing Angular web components, but then that part runs in a web view.
[05:27] The logic though can stay as long as it does not depend on browser APIs.
[05:32] Angular Native also went the extra mile and integrated Tailwind, the Angular Router, Hot Reload and a testing library.
[05:41] It supports the React Native build environment with the Bundler Metro and Expo, which is somewhat like what NX or Angular CLI is to Angular.
[05:53] So Angular doesn't just run on top of React Native, but it also unlocks the access to its ecosystem.

## block 20 topic 43 presenter 06:02-06:33
[06:01] If you are designing a UI library for general use, then you have to support different use cases and that can become quite complicated.
[06:11] For example, it might start with a simple string as an input.
[06:15] That could then expand to maybe also supporting a function, because the component is called within a context and we need access to that context.
[06:27] Then, users might want to add HTML, a template to it, or even a component.

## block 21 topic 45 presenter 06:33-06:39
[06:33] Think of a tooltip, for example.

## block 22 topic 45 screen 06:39-06:47
[06:36] You might have a simple title, but then this tooltip runs in a loop, and you want to access the current element or something.

## block 23 topic 46 presenter 06:47-06:53
[06:44] Later on, you can also say you maybe want to have certain HTML formatting to that particular tooltip.

## block 24 topic 47 presenter 06:53-07:01
[06:50] So if you are the author of such a component, a lot of work will go into that component to make it applicable to all those use cases.

## block 25 topic 48 screen 07:01-07:26
[07:01] Alex Inkin is a lead developer behind Tiger UI, and those kinds of challenges are his bread and butter, so to speak.
[07:10] Alex has published an article on Angular Space, where he discusses his library, PolymorphOS, which is optimized exactly for these challenges.
[07:21] It is used inside of TigerUI, and it can also be used by us.

## block 26 topic 51 presenter 07:26-07:32
[OTRA VOZ] [07:27] I wish you a nice weekend.
[OTRA VOZ] [07:28] See you in the next episode.
[07:29] Goodbye.

## block 27 topic 55 screen 07:32-07:35
