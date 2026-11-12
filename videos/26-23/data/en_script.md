# EN 26-23: 34 sentences, 03:49


## block 0 topic 0 presenter 00:00-00:06
[00:00] Hello, my name is Rainer Hanekamp, and this is NG News with the latest updates from the Angular community.

## block 1 topic 1 screen 00:06-00:18
[00:06] DevFrame is a library for creating dev tools, and it is already used outside of the Angular ecosystem.

## block 2 topic 1 presenter 00:18-00:27
[00:14] It was created by Anthony Fu, who is also the creator of btest, slidef, but also a core team member of Vue .js, Vite, and Nuxt.

## block 3 topic 2 screen 00:27-00:36
[00:27] Anthony announced their frame in September 2026.
[00:30] Now, one month later, Angular has a new tool built on it.

## block 4 topic 3 screen 00:36-00:42
[00:36] Pangular Inspector maintained by Erkam Yaman and Santosh Yadav.

## block 5 topic 4 screen 00:42-00:50
[00:42] Santosh has been around the Angular community for quite some time.
[00:46] He is a GitHub star, NX champion and Google developer expert.

## block 6 topic 5 screen 00:50-01:09
[00:50] Erkam maintains the Turkish translation of the Angular documentation and has recently contributed extensively to Angular Native, which we covered in the last episode.
[01:02] And he has also done the integration into Analog, which is a meta framework for Angular.

## block 7 topic 6 presenter 01:09-01:11
[01:09] Pingular wants to become the unified devtools for Angular.

## block 8 topic 6 screen 01:11-01:19
[01:13] Based on devframes, it can analyze the source code but also the live state.

## block 9 topic 7 screen 01:19-01:34
[01:19] It shows components, signals, NGRIX stores, services, forms and routes.
[01:25] Source scans tell you what is declared in your project.
[01:29] Live inspection shows the instances and values in the running application.

## block 10 topic 8 screen 01:34-01:42
[01:34] That information is available through its inspector panel and to your coding agent through MCP.

## block 11 topic 11 presenter 01:42-01:47
[01:42] And Alex Recurbel, the tech lead of the Angular framework gave also a talk at VidConf.

## block 12 topic 11 screen 01:47-01:58
[01:48] He shortly explained the history of Angular and then moved on to the current works on porting parts of the compiler to Rust and Oxy.

## block 13 topic 11 presenter 01:58-02:00

## block 14 topic 12 presenter 02:00-02:13
[02:00] We have already been discussing this in the last episode, but since Alex is the leader of the Angular framework, let's hear from him the direction they are taking now in terms of Angular and Rust.

## block 15 topic 13 screen 02:13-02:21
[02:13] That part is where most of the complexity is, where the time is spent.
[02:17] That's where the opportunity is.

## block 16 topic 14 screen 02:21-02:28
[02:19] So if we split our compiler this way, we could think about rewriting that expensive analysis portion in a native language like Rust and interface it with the node -based code generator.

## block 17 topic 15 screen 02:28-02:31

## block 18 topic 16 screen 02:31-02:34
[OTRA VOZ] [02:31] We chose Rust because of Oxy.

## block 19 topic 17 screen 02:34-02:44
[OTRA VOZ] [02:33] Oxy is void zero's JavaScript toolchain and it's amazing.
[OTRA VOZ] [02:38] It's become something of an ecosystem standard.

## block 20 topic 18 screen 02:44-02:55
[OTRA VOZ] [02:41] It's behind many of the modern JavaScript tools that we're talking about here, including Vite, and that matters to us because we want to build on something that's going to be stable and durable.

## block 21 topic 19 screen 02:55-03:03
[02:50] Compilation starts with a TS config, the same as before, but now we feed that to the Oxy -based Angular analyzer, ng -analyze, and that spits out metadata which we send to our node -based code generator, what we call the preprocessor.

## block 22 topic 20 screen 03:03-03:15
[03:06] And that code generator does one of two things.
[03:09] It either spits out a TypeScript file with runtime code or it spits out a different file with code meant for type checking or the language service.

## block 23 topic 21 screen 03:15-03:20

## block 24 topic 24 screen 03:20-03:45
[03:20] And Julian Yandel from PushBased gave a talk on server -side rendering and the recording is now available on YouTube.
[03:29] He presented his work that he and his colleagues did it on a betting platform, the challenges they encountered, and the solutions using custom strategies for incremental static regeneration, or ISR.

## block 25 topic 27 presenter 03:45-03:52
[03:45] And that's it.
[03:46] I wish you a nice week and see you in the next episode.
[03:48] Goodbye.

## block 26 topic 31 screen 03:52-03:55
