<!-- @format -->

Takes an existing Audacity macro that normalizes, adds compression setttings, and exports the file to create uniform volume across our recordings. This script opens Audacity, read in an mp3, run the macro, fix the ID3 tags that Audacity mangles, rename the exported file and move it to the original folder.

You must have the Audacity Pipe-Test file so it can be imported.

Relies heavily on work by:

The Audacity Pipe-Test:
https://github.com/audacity/audacity/blob/master/scripts/piped-work/pipe_test.py

And this one:
https://github.com/audacity/audacity/blob/master/scripts/piped-work/recording_test.py

And redditor /u/ColossalThrust:
https://www.reddit.com/r/audacity/comments/rrecu7/audiobook_piping_script/
