The following are guidelines to follow when working on the project. What specifically should be followed depends on if a particular piece was written by you or another party and how it is integrated into an IMAGE component.

* Code used as a library
    - If linked via a package manager (in `package.json`, `requirements.txt`, etc.) then there is nothing more to do.
    - Otherwise, include mention of it in a component-specific README and a link back to the project's page/repository.
* Code added as a file but NOT modified
    - Include mention of it in a component-specific README and link back to the project's page/repository.
* Code added as a file AND modified
    - Keep any authorship/copyright/license notice included in the file.
    - Add the [IMAGE project header](https://github.com/Shared-Reality-Lab/auditory-haptic-graphics-server/blob/438d72ba0c1cda54e0a634fad50a98100707770c/handlers/generic-tts-handler/src/server.ts#L1-L16) and below that indicate that this is a derivative work and where it came from.
* Code snippets added to an original file (e.g., from StackOverflow)
    - Clearly indicate where the section of code came from, ideally with a link.
    - If snippets from one source make up the bulk of the file, treat the entire file as a derivative work (see above). Otherwise, also follow the instructions for an original file (see below).
* Original file using only original code
    - [IMAGE project header](https://github.com/Shared-Reality-Lab/auditory-haptic-graphics-server/blob/438d72ba0c1cda54e0a634fad50a98100707770c/handlers/generic-tts-handler/src/server.ts#L1-L16)