import AppKit
import Foundation

// pbfile.swift
//
// Purpose:
// Copy local files/directories to the macOS pasteboard so they can be pasted in Finder.
//
// Design:
// 1. Primary path: write file URLs via NSPasteboard.writeObjects([NSURL]).
//    Apple documents URL pasteboard support via NSURL / NSPasteboard.
// 2. Compatibility path: also publish NSFilenamesPboardType.
//    This type is deprecated, but retained here because Finder paste behavior
//    was observed to be more reliable for some files/directories when it is present.
//
// Apple references:
// - NSPasteboard URL type:
//   https://developer.apple.com/documentation/appkit/nspasteboard/pasteboardtype/url
// - NSFilenamesPboardType (deprecated):
//   https://developer.apple.com/documentation/appkit/nsfilenamespboardtype
// - AppKit release notes for macOS 10.14:
//   https://developer.apple.com/documentation/macos-release-notes/appkit-release-notes-for-macos-10_14

let fm = FileManager.default
let cwd = URL(fileURLWithPath: fm.currentDirectoryPath, isDirectory: true)
let rawArgs = Array(CommandLine.arguments.dropFirst())

// Resolve inputs relative to the current working directory,
// expand "~", normalize paths, and remove duplicates.
let urls: [URL] = Array(
  NSOrderedSet(array: rawArgs.map { raw in
    let expanded = NSString(string: raw).expandingTildeInPath
    return URL(fileURLWithPath: expanded, relativeTo: cwd)
      .absoluteURL
      .standardizedFileURL
  })
)
.compactMap { $0 as? URL }
.filter { fm.fileExists(atPath: $0.path) }

guard !urls.isEmpty else {
  exit(0)
}

let pb = NSPasteboard.general
pb.clearContents()

// Modern AppKit path.
guard pb.writeObjects(urls as [NSURL]) else {
  fputs("fcopy: failed to write file URLs to pasteboard\n", stderr)
  exit(1)
}

// Finder compatibility fallback.
// Deprecated API, intentionally retained for observed paste reliability.
pb.setPropertyList(urls.map(\.path), forType: .init("NSFilenamesPboardType"))
