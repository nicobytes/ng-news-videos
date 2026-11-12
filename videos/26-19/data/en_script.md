# EN 26-19: 27 sentences, 04:05

[VOZ SIN TRANSCRIBIR] 03:23-03:26: leer en en_captions.png

## block 0 topic 0 presenter 00:00-00:55
[00:00] Hello, my name is Rainer Haneckamp, and this is NG News with the latest updates from the Angular community.
[00:06] Angular 22 .1 has been released, and as we have already discussed in a former episode, it is not going to be the only minor release in the 22 version range.
[00:18] Because of the new release cycle, which happens only once per year, we can now expect four to six minor versions.
[00:27] As a minor version, 22 .1 can only introduce new features but no breaking changes.
[00:36] And the main new feature is a set property of the linked signal that extends the linked signal so much that it could have actually been a new signal function.
[00:48] For the first time, we have something like a two -way binding for signals.

## block 1 topic 0 screen 00:55-03:30
[00:54] So, the use case is that we have here this Euro field, if I type something into Euro, the dollar gets updated and if I type something into the dollar, the Euro gets updated.
[01:05] How is that implemented?
[01:07] The USD, the signal that holds the dollar is a linked signal, which means whenever the Euro value changes, then also the dollar value changes and that happens immediately, synchronously.
[01:23] For
[01:25] the other way around, we have to use an effect, because until 2022 .1, there was no other choice.
[01:33] So in this case, the effect is listening for the USD value, and then in the untracked updates the Euro value.
[01:43] Unfortunately, that is done asynchronously, because it is an effect.
[01:49] And here we have a reset Euro that is a function which immediately sets the dollar value to the amount of 100.
[01:58] So what happens?
[02:00] If we go back and if we would now say, okay, we have here 10 dollars, then we have to look at the console because if we click now on this button and change USD value to 100, then we see that the euro has
[02:16] still the old value although of course in the input field it is not there but this is the typical asynchronous behavior of the effect which is very problematic
[02:30] now with this new version of the linked signal what we can do is that directly in the linked signal we cannot use the set property where we can immediately write back to the euro value if the value in the usd field has been
[02:52] changed and
[02:59] once we have done that we can also get rid of the effect because we don't need it anymore the linked signal is now doing all the work work.
[03:09] So again, same example as before, we're typing something into Euro, we are setting dollar to 100 and we see that now in the console the Euro is also updated immediately synchronously
[03:26] as it should be.

## block 2 topic 0 presenter 03:30-04:01
[03:29] You could even use it to work around the glitch -free effect, which means you would have the option to be notified about a signal change when it happened multiple times and synchronously.
[03:43] I think we can be pretty sure that this was not the original intention of that feature.
[03:50] Obviously, we also got other features and bug fixes, but for those cases just please consult your common videos, blogs and articles.

## block 3 topic 1 presenter 04:01-04:03
[04:01] That's it. I wish you a nice week and see you in the next episode.

## block 4 topic 2 presenter 04:03-04:05
[04:04] Goodbye.
